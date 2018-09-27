# ansible 配置文档
请注意
**只需要在运维服务器上部署ansible即可**

部署多链时需要用到ansible进行多服务器的数据流传输，ansible是基于Python开发，集合了众多运维工具（puppet、cfengine、chef、func、fabric）的优点，实现了批量系统配置、批量程序部署、批量运行命令等功能的一个自动化运维工具。本文是多链物料包ansible的配置文档。

## 安装
centOS系统
```
配置EPEL
yum install https://dl.fedoraproject.org/pub/epel/epel-release-latest-7.noarch.rpm
sudo yum install ansible
```
ubuntu系统
```
$ sudo apt-get install software-properties-common
$ sudo apt-add-repository ppa:ansible/ansible
$ sudo apt-get update
$ sudo apt-get install ansible
```

## 配置
配置前需要确保与对应主机可以进行ssh通信,物料包使用的ansible通信方式自动公钥认证方式，因此用户需要执行以下命令配置ssh密钥。

```
$ ssh-keygen -t rsa
$ cp id_rsa  id_rsa.pub ~/.ssh/
$ vim hostsname.txt
```
创建hostsname.txt格式如下
```
user 127.0.0.1 22 123
user 127.0.0.2 80 123
user 127.0.0.3 36000 123
```
第一项为用户名，第二项为ip 第三项为端口号，第四项为密码

```
$ bash ssh-copy-id.sh
$ ssh-agent bash
$ ssh-add ~/.ssh/id_rsa
```

在文件最后添加

配置完key后，需要在sshd_config文件中开启key认证
```
$ vim /etc/ssh/sshd_config
PubkeyAuthentication yes  //将该项改为yes 
```
修改完成后，通过/etc/init.d/sshd restart 重启ssh服务重新加载配置。如果想要禁用密码认证，更改如下项：
```
$ vim /etc/ssh/sshd_config
UsePAM yes
为
UserPAM no
```
添加托管服务器ip至ansible配置中
```
vim /etc/ansible/hosts
127.0.0.1 ansible_ssh_user=auser_name ansible_ssh_pass='user@passwd' ansible_port=36000

127.0.0.2 ansible_ssh_user=auser_name ansible_ssh_pass='user@passwd' ansible_port=36000

127.0.0.3 ansible_ssh_user=auser_name ansible_ssh_pass='user@passwd' ansible_port=36000

127.0.0.4 ansible_ssh_user=auser_name ansible_ssh_pass='user@passwd' ansible_port=36000
```
127.0.0.1为托管后患服务器ip

ansible_ssh_user=auser_name 为托管服务器用户名 auser_name为用户需要配置的用户名

ansible_ssh_pass='user@passwd' user@passwd为与托管服务器进行ssh通信的密码

ansible_port=36000 为域托管服务器进行ssh通信的端口号 如36000 如果不设置，默认使用22端口进行ssh通信

上述配置中，用户可以通过 用户名为auser_name 的用户，与127.0.0.1，127.0.0.2，127.0.0.3，127.0.0.4进行端口号为36000的ssh通信，ssh的通信密码为user@passwd

## 检测
配置完成之后，使用下述命令进行测试
```
$ ansible all -m ping
```

如果正确会输出下述标准输出

```
127.0.0.1 | SUCCESS => {
    "changed": false, 
    "ping": "pong"
}
127.0.0.2 | SUCCESS => {
    "changed": false, 
    "ping": "pong"
}
127.0.0.3 | SUCCESS => {
    "changed": false, 
    "ping": "pong"
}
127.0.0.4 | SUCCESS => {
    "changed": false, 
    "ping": "pong"
}
```