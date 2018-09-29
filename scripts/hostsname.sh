#!/bin/bash
mv /etc/ansible/hosts /etc/ansible/hosts.bak
cat ./conf/hosts.conf | while read user ip port passwd
do
echo -n $ip >> /etc/ansible/hosts
echo -n " ansible_ssh_user="$user >> /etc/ansible/hosts
echo -n " ansible_port="$port >> /etc/ansible/hosts
echo " ansible_ssh_pass="$passwd >> /etc/ansible/hosts
done