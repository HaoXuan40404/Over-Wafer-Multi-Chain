#!/bin/bash
# dirpath="$(cd "$(dirname "$0")" && pwd)"
# cd $dirpath

hosts_conf=$1
if [ ! -f ${hosts_conf} ];then
    echo " hosts_conf not exist, host_conf is ${hosts_conf}"; exit 1;
fi

sudo mv /etc/ansible/hosts /etc/ansible/hosts.bak
cat ${hosts_conf} | while read user ip port passwd
do
echo -n $ip | sudo tee -a /etc/ansible/hosts
echo -n " ansible_ssh_user="$user | sudo tee -a /etc/ansible/hosts
echo -n " ansible_port="$port | sudo tee -a /etc/ansible/hosts 
echo " ansible_ssh_pass="$passwd | sudo tee -a /etc/ansible/hosts 
echo "[$ip]:36000 ecdsa-sha2-nistp256 AAAAE2VjZHNhLXNoYTItbmlzdHAyNTYAAAAIbmlzdHAyNTYAAABBBA0hhTKXKn4brChqhd3wtdbWpwiipbOK/wTRGmxX7uuo8kxUGGrLUl35CamwIvtGpngCVVMnKdeZfu4aPARXDX0=" >> ~/.ssh/known_hosts
done