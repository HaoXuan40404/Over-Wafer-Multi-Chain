#!/usr/bin/env bash
cat ./conf/hosts.conf | while read user ip port passwd
do
sshpass -p ${passwd} ssh-copy-id -i ~/.ssh/id_rsa.pub -p ${port} ${user}@${ip} >/dev/null 2>&1 & 
done
ssh-agent bash
ssh-add ~/.ssh/id_rsa