import sys

import docker

sys.path.append(".")

# fmt: off
from config.docker import settings

# fmt: on

here = settings.host_url

EACH_NUMBER = 4


def get_number(id):
    # id += 20000
    return f"172.{233+id}.0.0/16"


def get_number2(id):
    return f"255.{(20000+id)//256}.{(20000+id)%256}.0/24"


SS = 0
client_here = docker.DockerClient(base_url=here)


traefik_subnet = client_here.networks.create(
    "traefik_subnet",
    driver="overlay",
    ipam=docker.types.IPAMConfig(
        pool_configs=[
            docker.types.IPAMPool(
                subnet=get_number(0),  # 最顶层的外网
            )
        ],
    ),
    attachable=True,
    internal=False,
    scope="swarm",
)

traefik_master = client_here.services.create(
    image="traefik:v2.5",
    name="traefik-master",
    args=[
        "--api.insecure=true",
        "--providers.docker.swarmMode=true",
        f"--providers.docker.endpoint={here}",
        # "--providers.docker.swarmModeRefreshSeconds=1",
        "--providers.docker=true",
        "--providers.docker.exposedbydefault=false",
        "--entrypoints.master.address=:80",
        "--providers.docker.network=traefik_subnet",
        "--providers.docker.constraints=Label(`connected_master`, `master`)",
    ],
    endpoint_spec={
        "Ports": [
            {"Protocol": "tcp", "PublishedPort": 8080, "TargetPort": 8080},
            {"Protocol": "tcp", "PublishedPort": 80, "TargetPort": 80},
        ]
    },
    # mounts=[
    #     {
    #         "Source": "/var/run/docker.sock",
    #         "Target": "/var/run/docker.sock",
    #         "Type": "bind",
    #     }
    # ],
    networks=[traefik_subnet.id],
    mode=docker.types.ServiceMode("replicated", replicas=1),
)

client = client_here
for it in range(3):
    try:
        service_old = client.services.list(filters={"name": f"traefik-slaver-{it}"})[0]
        service_old.remove()
    except Exception:
        pass

    reserved_subnets = []
    for _ in range(EACH_NUMBER):
        print(it, _)
        SS += 1
        reserved_subnet = client.networks.create(
            f"traefik_reserved_subnet_{it}_{_}",
            driver="overlay",
            ipam=docker.types.IPAMConfig(
                pool_configs=[
                    docker.types.IPAMPool(
                        subnet=get_number2(SS + 1),
                    )
                ],
            ),
            attachable=True,
            internal=False,
        )
        reserved_subnets.append(reserved_subnet.id)

    traefik_slave_slave = client.services.create(
        image="traefik:v2.5",
        name=f"traefik-slave-{it}",
        args=[
            "--api.insecure=true",
            "--providers.docker=true",
            f"--providers.docker.endpoint={here}",
            "--providers.docker.swarmMode=true",
            "--providers.docker.exposedbydefault=false",
            f"--providers.docker.constraints=Label(`connected_slave_id`, `{it}`)",
            "--providers.docker.swarmModeRefreshSeconds=5",
            f"--entrypoints.slave{it}.address=:80",
        ],
        labels={
            "traefik.enable": "true",
            "traefik.docker.network": "traefik_subnet",
            # 需要修改域名
            f"traefik.http.routers.slave{it}.rule": f"HostRegexp(`{{host:.+{it}\\.test\\.thudart\\.com}}`)",
            f"traefik.http.routers.slave{it}.entrypoints": "master",
            f"traefik.http.services.slave{it}.loadbalancer.server.port": "80",
            # 需要修改域名
            "suffix_hostname": f"{it}.test.thudart.com",
            "slave": f"{it}",
            "connected_master": "master",
        },
        # mounts=[
        #     {
        #         "Source": "/var/run/docker.sock",
        #         "Target": "/var/run/docker.sock",
        #         "Type": "bind",
        #     }
        # ],
        mode=docker.types.ServiceMode("replicated", replicas=1),
        networks=reserved_subnets + [traefik_subnet.id],
    )