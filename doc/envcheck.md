# 环境依赖

本章内容包括用户的操作系统检测以及启动fisco bcos需要的环境检测

在使用OWMC物料包之前，需要确保所有电脑的操作系统满足fisco bcos1.3版本的运行条件, OWMC物料包会对环境进行检测，但是不会对相关依赖进行安装。


* 机器配置
  
  参考FISCO BCOS的[机器配置](https://github.com/FISCO-BCOS/FISCO-BCOS/tree/master/doc/manual#%E7%AC%AC%E4%B8%80%E7%AB%A0-%E9%83%A8%E7%BD%B2fisco-bcos%E7%8E%AF%E5%A2%83)

## 环境CheckList 
FISCO BCOS对网络、yum源等外部环境存在依赖, 为减少搭建过程中遇到的问题,建议在使用之前对整个搭建的环境进行检查。  

### 检查项
- 操作系统
- 网络
- openssl版本
- yum/apt源检查

#### 操作系统  
```
支持操作系统：
CentOS 7.2 64位 、 Ubuntu 16.04 64位
```
- 检查系统是否为64位系统：  
使用**uname -m**命令, 64位系统的输出为x86_64, 32位系统的输出为i386或者i686.
```
$ uname -m
$ x86_64
```

- 操作系统版本检查：
```
CentOS
$ cat /etc/redhat-release 
$ CentOS Linux release 7.2.1511 (Core)

Ubuntu
$ cat /etc/os-release
$ NAME="Ubuntu"
$ VERSION="16.04.1 LTS (Xenial Xerus)"
$ ID=ubuntu
$ ID_LIKE=debian
$ PRETTY_NAME="Ubuntu 16.04.1 LTS"
$ VERSION_ID="16.04"
$ HOME_URL="http://www.ubuntu.com/"
$ SUPPORT_URL="http://help.ubuntu.com/"
$ BUG_REPORT_URL="http://bugs.launchpad.net/ubuntu/"
```

#### 网络 
FISCO BCOS单节点需要使用三个端口： rpc_port、channel_port、p2p_port.  
- rpc_port不会有远程访问.  
- channel_port需要被使用web3sdk的服务访问.  
- p2p_port 节点之间通过互联组成p2p网络.  
- 
**实际中, 需要考虑channel_port、p2p_port的网络访问策略, 节点的channel_port需要被使用区块链服务的应用所在服务器连接, 
每个节点的p2p_port需要能被其他节点所在服务器的连接.**

检查服务器A某一个端口p能够被另一台服务器B访问的简单方法：
- 1. 在服务器A上执行.
```
sudo nc -l num    //实际检查时, 将num替换为实际端口.
```
- 2. 在服务器B上面执行telnet命令.
```
$ telnet A num  //实际检查时, 将A替换服务器ip, 将num替换为实际端口.
Trying A...
Connected to A.
Escape character is '^]'.
```
上面的结果说明成功, 服务器B确实可以访问服务器A的端口num.

- 3. 网络不通, 通常需要运维工程师协助解决.


#### openssl版本
openssl需求版本为1.0.2, 可以使用 openssl version 查看.
```
$ openssl version
$ OpenSSL 1.0.2k-fips  26 Jan 2017
```

服务器如果没有安装openssl, 可以使用yum/apt进行安装.
```
sudo yum/apt -y install openssl
```
yum/apt不存在openssl, 可以参考下面的替换apt/yum源.

#### yum/apt源检查 
物料包工作过程中会使用yum/apt安装一些依赖项, 当前yum/apt源无法下载到相关依赖时, 工作工程中可能会出现一些问题,
对此建议可以提前检查yum/apt镜像仓库。 

如果apt/yum安装某些项失败, 说明apt/yum源不存在该依赖项.



- CentOS安装案例云进行仓库
```
$ wget http://dl.fedoraproject.org/pub/epel/epel-release-latest-7.noarch.rpm
$ rpm -ivh epel-release-latest-7.noarch.rpm
$ yum repolist      ##检查是否已添加至源列表
```

- Ubuntu 配置software-properties-common  
```
$ sudo apt-get update
$ sudo apt-get -y install apt-transport-https ca-certificates curl software-properties-common
$ curl -fsSL http://mirrors.aliyun.com/docker-ce/linux/ubuntu/gpg | sudo apt-key add -
之后输入软件源信息

```



