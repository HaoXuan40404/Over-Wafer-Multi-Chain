#!/bin/bash

user=$1
ip=$2
port=$3
passwd=$4

type ansible >/dev/null 2>&1 
if [ $? -ne 0 ];then
    echo 'ansible not installed, pls check it'
    exit 1
fi
sudo echo ''
if [ $? -ne 0 ];then
    echo 'sudoer permission failure'
    exit 1
fi
echo -n $ip | sudo tee -a /etc/ansible/hosts
echo -n " ansible_ssh_user="$user | sudo tee -a /etc/ansible/hosts
echo -n " ansible_port="$port | sudo tee -a /etc/ansible/hosts 
echo " ansible_ssh_pass="$passwd | sudo tee -a /etc/ansible/hosts 
echo "[$ip]:36000 ecdsa-sha2-nistp256 AAAAE2VjZHNhLXNoYTItbmlzdHAyNTYAAAAIbmlzdHAyNTYAAABBBA0hhTKXKn4brChqhd3wtdbWpwiipbOK/wTRGmxX7uuo8kxUGGrLUl35CamwIvtGpngCVVMnKdeZfu4aPARXDX0=" >> ~/.ssh/known_hosts
sshpass -p ${passwd} ssh-copy-id -i ~/.ssh/id_rsa.pub -p ${port} ${user}@${ip} >/dev/null 2>&1 
if [ $? -ne 0 ];then
    echo 'sshpass failure'
    exit 1
fi
eval `ssh-agent -s`
ssh-add ~/.ssh/id_rsa
if [ $? -ne 0 ];then
    echo 'ssh-add failure'
    exit 1
fi

