#!/usr/bin/env bash
cat hostsname.txt | while read user ip port passwd
do
sshpass -p $passwd ssh-copy-id  -i ~/.ssh/id_rsa -p ${port} username@${ip}
done