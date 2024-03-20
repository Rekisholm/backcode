#!/bin/bash

container_ids=$(docker ps -q)

statement="sysdig -s 0 -p\"*%evt.datetime %proc.name %proc.pid %proc.vpid %evt.dir %evt.type %fd.name %proc.ppid %proc.exepath %evt.rawres %fd.lip %fd.rip %fd.lport %fd.rport %evt.info %container.id %container.name\" \"container.name!=host and"

is_first=true
for container_id in $container_ids; do
    if $is_first; then
        statement="$statement (container.id=$container_id"
        is_first=false
    else
        statement="$statement or container.id=$container_id"
    fi
done
statement="$statement )\" -j -w log_container.scap"

echo "$statement" > sysdig_cmd_0916.sh
chmod +x sysdig_cmd_0916.sh
