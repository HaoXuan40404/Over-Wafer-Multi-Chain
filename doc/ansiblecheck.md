# ansible 配置文档
请注意
**只需要在运维服务器上部署ansible即可**

部署OWMC时需要用到ansible进行多服务器的数据流传输。本文是OWMC物料包ansible的配置文档。

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
配置前需要服务起之间可以进行ssh通信,OWMC运维服务器与后台服务器通信之间使用公钥认证方式，因此用户需要执行以下命令配置ssh密钥。


以下命令请使用默认设置，输入三次回车即可
```
$ ssh-keygen -t rsa
```

P.S. 生成的密钥会在owmc的init命令中使用

需要在sshd_config文件中开启key认证
```
$ vim /etc/ssh/sshd_config
PubkeyAuthentication yes  //将该项改为yes 
```
修改完成后，通过sudo service sshd restart重启ssh服务重新加载配置。

## 检测
配置完成之后，使用下述命令进行测试，用以检测用户的ansible是否安装成功。其中127.0.0.1不需要替换
```
$ ansible 127.0.0.1 -m ping
```
如果程序正确安装会输出下述标准输出

```
127.0.0.1 | SUCCESS => {
    "changed": false, 
    "ping": "pong"
}

```

## ansible配置相关

关于ansible配置的更多问题或希望了解关于ansible更多的操作，可以参考[ansible官方文档](https://ansible-tran.readthedocs.io/en/latest/)
