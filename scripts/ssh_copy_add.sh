#!/usr/bin/env bash
cat ./conf/hosts.conf | while read user ip port passwd
do
sshpass -p ${passwd} ssh-copy-id  -i ~/.ssh/id_rsa -p ${port} ${user}@${ip}
done
ssh-agent bash
ssh-add ~/.ssh/id_rsa