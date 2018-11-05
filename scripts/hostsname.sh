#!/bin/bash
# dirpath="$(cd "$(dirname "$0")" && pwd)"
# cd $dirpath

hosts_conf=$1
if [ ! -f ${hosts_conf} ];then
    echo " hosts_conf not exist, host_conf is ${hosts_conf}"; exit 1;
fi

mv /etc/ansible/hosts /etc/ansible/hosts.bak
cat ${hosts_conf} | while read user ip port passwd
do
echo -n $ip >> /etc/ansible/hosts
echo -n " ansible_ssh_user="$user >> /etc/ansible/hosts
echo -n " ansible_port="$port >> /etc/ansible/hosts
echo " ansible_ssh_pass="$passwd >> /etc/ansible/hosts
done