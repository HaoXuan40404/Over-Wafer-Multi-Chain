#!/bin/bash

hosts_conf=$1
if [ ! -f ${hosts_conf} ];then
    echo " hosts_conf not exist, host_conf is ${hosts_conf}"; exit 1;
fi

cat ${hosts_conf} | while read user ip port passwd
do
sshpass -p ${passwd} ssh-copy-id -i ~/.ssh/id_rsa.pub -p ${port} ${user}@${ip} >/dev/null 2>&1 & 
done
eval `ssh-agent`
ssh-add ~/.ssh/id_rsa
exit 0