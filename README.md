# FISCO BCOS 物理多链物料包使用手册


<!-- TOC -->

- [FISCO BCOS 物理多链物料包使用手册](#fisco-bcos-物理多链物料包使用手册)
    - [介绍](#介绍)
        - [配置ansible](#配置ansible)
        - [功能简介](#功能简介)
        - [依赖](#依赖)
        - [版本支持](#版本支持)
    - [部署多链](#部署多链)
        - [下载物料包](#下载物料包)
        - [配置](#配置)
            - [配置详解](#配置详解)
        - [创建安装包](#创建安装包)
        - [部署安装包](#部署安装包)
        - [部署节点](#部署节点)
        - [启动节点](#启动节点)
        - [验证节点](#验证节点)
        - [启动节点](#启动节点-1)
        - [问题排查](#问题排查)
    - [扩容多链](#扩容多链)
        - [场景分析](#场景分析)
        - [获取扩容文件](#获取扩容文件)
        - [配置](#配置-1)
        - [生成扩容安装包](#生成扩容安装包)
        - [部署库容节点](#部署库容节点)
        - [扩容节点注册](#扩容节点注册)
        - [问题排查](#问题排查-1)
    - [其他工具配置](#其他工具配置)
        - [[web3sdk配置](https://github.com/ywy2090/fisco-package-build-tool/blob/docker/doc/web3sdk.md)](#web3sdk配置httpsgithubcomywy2090fisco-package-build-toolblobdockerdocweb3sdkmd)
            - [操作说明](#操作说明)
            - [配置说明](#配置说明)
        - [[环境checklist](https://github.com/ywy2090/fisco-package-build-tool/blob/docker/doc/物料包环境搭建CheckList.md)](#环境checklisthttpsgithubcomywy2090fisco-package-build-toolblobdockerdocchecklistmd)

<!-- /TOC -->
## 介绍

### 配置ansible
运维服务器部署ansible
以centos7位例

```
yum install https://dl.fedoraproject.org/pub/epel/epel-release-latest-7.noarch.rpm
sudo yum install ansible
```
使用ansible之前，需要对托管服务器配置运维服务器的RSA公钥，操作如下：
运维服务器上操作：
```
$ ssh-keygen -t rsa
$ cp id_rsa  id_rsa.pub ~/.ssh/
$ ssh-copy-id  -i ~/.ssh/id_rsa username@xxx,xxx,xxx,xx
```
xxx,xxx,xxx,xx为对应服务器的ip

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
物料包操作
基本操作 
```
### 部署多链
$git clone https://github.com/ywy2090/multi-chain.git
cd multi-chain
python main.py -h
```
可以查询到相关的操作命令
```
usage: main.py [-h] [--version] [--build ./config.conf or ./conf/ fisco_path]
               [--pkg_list all or chain_id or [chain_id_1 chain_id_2 ...]]
               [--pub_list all or chain_id or [chain_id_1 chain_id_2 ...]]
               [--publish chain_id:version eg. [chain_id_1:version_1 chain_id_2:version_1 chain_id_3:version_2.etc. ...]]
               [--check all or chain_id or [chain_id:host_ip ...]]
               [--stop all or chain_id or [chain_id:host_ip ...]]
               [--start all or chain_id or [chain_id:host_ip ...]]
               [--monitor all or chain_id or [chain_id:host_ip ...]]
               [--chainca ./dir_chain_caSET)]
               [--agencyca ./dir_agency_ca(SET) ./chain_ca_dir The Agency Name]
               [--sdkca ./dir_sdk_ca(SET ./dir_agency_ca]
               [--echo all or host_ip or [host_ip1 host_ip2 ...]]

Description of multi-chain usage.

optional arguments:
  -h, --help            show this help message and exit
  --version             version of multi-chain
  --build ./config.conf or ./conf/ fisco_path
                        Output => package. Build all package under directory
                        ./data/chain/ according to the input.
  --pkg_list all or chain_id or [chain_id_1 chain_id_2 ...]
                        Output => list all build package info.
  --pub_list all or chain_id or [chain_id_1 chain_id_2 ...]
                        Output => list all publish info.
  --publish chain_id:version eg. [chain_id_1:version_1 chain_id_2:version_1 chain_id_3:version_2.etc. ...]
                        Output => publish all package to servers
  --check all or chain_id or [chain_id:host_ip ...]
                        Output => check servers status
  --stop all or chain_id or [chain_id:host_ip ...]
                        Output => stop node
  --start all or chain_id or [chain_id:host_ip ...]
                        Output => start node
  --monitor all or chain_id or [chain_id:host_ip ...]
                        Output => monitor node
  --chainca ./dir_chain_ca(SET)
                        Output => the cert of chain that set on the SET
                        directory
  --agencyca ./dir_agency_ca(SET) ./chain_ca_dir The Agency Name
                        Output => the cert of agency that set on the SET
                        directory
  --sdkca ./dir_sdk_ca(SET) ./dir_agency_ca
                        Output => the cert of sdk for agency that set on the
                        SET directory
  --echo all or host_ip or [host_ip1 host_ip2 ...]
                        Output => test ansible of servers is useful or not
```
首先更改./conf 目录下的sample_12345_v1.0.conf文件，如果需要部署多条链，需要拷贝多个conf文件。

其中chainid必须为整形，chain version为string类型

logging.conf 暂时不需要关注。

mchain.conf为相关的部署目录和机构名称，用户根据需要修改。

相关操作，详见后期讲解。

使用前需要确保运维服务器可以启动1.3版本的fisco-bcos，并且对应服务器的环境可以启动fisco-bcos


1. 生成多链安装包

```
$python main.py --build ./conf/sample_12345_v1.0.conf $PATH/fisco-bcos
or
$python main.py --build ./conf $PATH/fisco-bcos
```
如果要生成某一条的链安装包执行第一个命令，如果在该目录下有多个安装包的conf文件，则执行第二条命令。build命令第二项参数为fisco-bcos的路径

生成的安装包在./data/chain 目录下

1.1 检查ansible配置
```
python main.py --echo all or host_ip or [host_ip1 host_ip2 ...]
```
监测ansible配置的所有服务器是否可以进行通信

2. 部署多链安装包

```
$python main.py --publish chain_id_1:version_1 chain_id_2:version_2 ...
```
chain_id_n:version_n 为chain的id和版本号，中间用":"隔开

3. 启动多链

```
$python main.py --start [all or chain_id or chain_id:host_ip]
```

三种参数分别对应启动部署的所有链的节点，部署的对应chain_id链的节点，和对应chain_id的host_ip的服务器的节点

4. 检查多链节点
```
$python main.py --check [all or chain_id or chain_id:host_ip]
```
操作同上

5. 停止多链节点
```
$python main.py --stop [all or chain_id or chain_id:host_ip]
```
操作同上

6. 列出生成安装包的节点
```
$python main.py --pkg_list [all or chain_id]
```
列出所有或者某一条链

7. 列出部署安装包的节点
```
$python main.py --pub_list [all or chain_id]
```
操作同上

8. ca证书相关操作

支持用户生成相关的证书在相关路径








-------------------------------------------------------------------------------------------------------------------------------------------------
下面还没完成 不用看
### 功能简介


FISCO BCOS 物理多链是针对机构内同时部署多条链的物料包。操作者可以在单台运维服务器上通过配置ssh与多台服务器进行交互，从而快速在多台服务器上部署多条区块链。

列如：在一台服务器上，配置好与其他服务器的ssh密钥，生成三条链，每条链在三台服务器上有三个节点，讲安装包推给对应服务器，启动节点，组成三个区块链网络。


### 依赖
* 机器配置
* 
  参考FISCO BCOS的[机器配置](https://github.com/FISCO-BCOS/FISCO-BCOS/tree/master/doc/manual#%E7%AC%AC%E4%B8%80%E7%AB%A0-%E9%83%A8%E7%BD%B2fisco-bcos%E7%8E%AF%E5%A2%83)

  ```
  支持的系统：

  CentOS 7 64位

  Ubuntu 16.04 64位
  ```

* 软件依赖
  
使用物料包时请先使用[CheckList](https://github.com/FISCO-BCOS/fisco-package-build-tool/blob/master/doc/%E7%89%A9%E6%96%99%E5%8C%85%E7%8E%AF%E5%A2%83%E6%90%AD%E5%BB%BACheckList.md)对当前环境进行检查
```
Oracle JDK[1.8]
Ansible
python2.7
```
**依赖说明**
* FISCO BCOS搭建过程中需要的其他依赖会自动安装, 用户不需要再手动安装

* CentOS/Ubuntu默认安装或者使用yum/apt安装的是openJDK, 并不符合使用要求, Oracle JDK 1.8 的安装链接[ Oracle JDK 1.8 安装](https://github.com/FISCO-BCOS/fisco-package-build-tool/blob/master/doc/Oracle%20JAVA%201.8%20%E5%AE%89%E8%A3%85%E6%95%99%E7%A8%8B.md)
  
* Ansible配置
* **只需要在运维服务器上部署ansible即可**
  
部署多链时需要用到ansible进行多服务器的数据流传输，ansible是基于Python开发，集合了众多运维工具（puppet、cfengine、chef、func、fabric）的优点，实现了批量系统配置、批量程序部署、批量运行命令等功能的一个自动化运维工具。


```
配置EPEL
yum install https://dl.fedoraproject.org/pub/epel/epel-release-latest-7.noarch.rpm
sudo yum install ansible
```

* 其他依赖
sudo权限, 当前执行的用户需要具有sudo权限，此外系统应至少安装python2.7

### 版本支持

多链物料包的版本号为1.x，支持用户进行回退操作。

## 部署多链
本章节主要讲解如何部署物理多链

### 下载物料包
```
$ git clone https://github.com/HaoXuan40404/py_temp_test.git
```
目录结构以及主要配置文件作用：
```
├── bin
├── ext
├── node
│   ├── node0
│   │   ├── conf
│   │   ├── data
│   │   └── log
│   └── node1
│       ├── conf
│       ├── data
│       └── log
├── pytools
├── scripts
└── web3sdk
```

### 配置
```
$cd package
$vim config_chain.ini
```
配置文件config_chain.ini
```
; 节点信息
[nodes]
; 格式为 : nodeIDX=p2p_ip listen_ip num agent
; IDX为索引, 从0开始增加.
; p2p_ip     => 服务器上用于p2p通信的网段的ip.
; listen_ip  => 服务器上的监听端口, 用来接收rpc、channel的链接请求, 建议默认值为"0.0.0.0".
; num        => 在服务器上需要启动的节点的数目.
; agent      => 机构名称, 若是不关心机构信息, 值可以随意, 但是不可以为空.
node0=0.107.105.137  0.0.0.0  4  agent
node1=0.107.105.81  0.0.0.0  4  agent
node2=0.107.105.141  0.0.0.0  4  agent

;端口配置, 一般不用做修改, 使用默认值即可.
[ports]
; p2p端口
p2p_port=30303
; rpc端口
rpc_port=8545
; channel端口
channel_port=8821

; 扩容使用的一些参数
[expand]
genesis_follow_dir=/follow/

[web3sdk]
keystore_pwd=123456
clientcert_pwd=123456
```
#### 配置详解
上述ini文件为一条链的配置文件，多条链需要多个配置和文件
* [nodes]部分
```
需要部署FISCO BCOS服务器上的节点配置信息.
[nodes]
; 格式为 : nodeIDX=p2p_ip listen_ip num agent
; IDX为索引, 从0开始增加.
; p2p_ip     => 服务器上用于p2p通信的网段的ip.
; listen_ip  => 服务器上的监听端口, 用来接收rpc、channel的链接请求, 建议默认值为"0.0.0.0".
; num        => 在服务器上需要启动的节点的数目.
; agent      => 机构名称, 若是不关心机构信息, 值可以随意, 但是不可以为空.
```

* [ports]部分
```
[ports]
; p2p端口
p2p_port=30303
; rpc端口
rpc_port=8545
; channel端口
channel_port=8821
```
fisco-bcos的每个节点需要使用3个端口,p2pport、rpcport、channelport, [ports]配置的端口是服务器上面的第一个节点使用的端口,其他节点依次递增.
```
node0=0.107.105.137 0.0.0.0 4 agent
```
上面的配置说明要在0.107.105.137服务器上启动四个节点, 按照默认的配置：

* 第1个节点的端口：p2p 30303、rpc 8545、channel 8821
* 第2个节点的端口：p2p 30304、rpc 8546、channel 8822
* 第3个节点的端口：p2p 30305、rpc 8547、channel 8823
* 第4个节点的端口：p2p 30306、rpc 8548、channel 8824
  
下面以在三台服务器上部署区块链为例构建一条新链：
```
服务器ip  ： 172.20.245.42 172.20.245.43 172.20.245.44  
机构分别为： agent_0   agent_1    agent_2  
节点数目  ： 每台服务器搭建两个节点
```
修改[nodes]部分字段为
```
[nodes]
node0=172.20.245.42  0.0.0.0  2  agent_0
node1=172.20.245.43  0.0.0.0  2  agent_1
node2=172.20.245.44  0.0.0.0  2  agent_2
```
生成的多个config_chain.ini文件需要放在config文件夹下，命名方式为为：config_chain_1.ini,config_chain_2.ini,...,config_chain_n.ini
### 创建安装包
```

```
执行成功之后会生成build目录, 目录下有生成的对应服务器的安装包：
```
├── build
│   ├── chain_1
│   │   ├── 127.0.0.1_agent_0
│   │   ├── 127.0.0.2_agent_1
│   │   └── 127.0.0.3_agent_3
│   ├── chain_2
│   │   ├── 127.0.0.1_agent_0
│   │   ├── 127.0.0.4_agent_1
│   │   └── 127.0.0.7_agent_2
│   └── chain_3
│       ├── 127.0.0.9_agent_0
│       ├── 127.0.0.2_agent_2
│       └── 127.0.0.3_agent_3
```

### 部署安装包
将安装包上传到对应服务器的过程需要保证运维服务器可以使用ssh与托管服务器通信。
使用ansible之前，需要对托管服务器配置运维服务器的RSA公钥，操作如下：
运维服务器上操作：
```
$ ssh-keygen -t rsa
$ cp id_rsa  id_rsa.pub ~/.ssh/
$ ssh-copy-id  -i ~/.ssh/id_rsa username@xxx,xxx,xxx,xx
```
xxx,xxx,xxx,xx为对应服务器的ip

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
之后添加托管服务器ip至ansible配置中
```
vim /etc/ansible/hosts
```
修改如下图所示：
```
[servers]
127.0.0.1 ansible_ssh_user=user  ansible_sudo_pass='123'
127.0.0.2 ansible_ssh_user=user  ansible_sudo_pass='123'
127.0.0.3 ansible_ssh_user=user  ansible_sudo_pass='123'
```
[servers]为分组名，可以忽略。

为托管后患服务器ip

ansible_ssh_user=user 为托管服务器用户名

ansible_sudo_pass='123' 为托管服务器sudo权限密码



配置完ssh通信之后，在安装目录下，执行：
```
$python unarchive.py
```
该命令会将安装包压缩推到对应服务器上，每台托管服务器都会接收到对应的安装包压缩文件并将其解压。
### 部署节点
在运维服务器安装目录下，执行
```
$python build.py
```
正确执行会在运维服务器上返回"chain_x,xxx,xxx,xxx,xx,build successful"
同时在对应托管服务器上新增build文件夹,build文件夹下包含node启动的相关配置文件
### 启动节点
在运维服务器安装目录下，执行
```
$python start.py
```

### 验证节点
预留功能

```
python check.py
```
执行后可以看到对应服务器的状态
```
python monitor.py
```
执行后可以看到节点的状态

### 启动节点
在运维服务器安装目录下，执行
```
$python stop.py
```

### 问题排查

参考FAQ

## 扩容多链

预留功能

### 场景分析

### 获取扩容文件

### 配置

### 生成扩容安装包

### 部署库容节点

### 扩容节点注册

### 问题排查

## 其他工具配置

### [web3sdk配置](https://github.com/ywy2090/fisco-package-build-tool/blob/docker/doc/web3sdk.md)
多链物料包内置了配置好的web3sdk以及相关的环境，操作者可以通过配置好的命令访问对应链的sdk

#### 操作说明

#### 配置说明

### [环境checklist](https://github.com/ywy2090/fisco-package-build-tool/blob/docker/doc/%E7%89%A9%E6%96%99%E5%8C%85%E7%8E%AF%E5%A2%83%E6%90%AD%E5%BB%BACheckList.md)
在搭建物料包时需要先进行环境监测，操作者在安装目录下，执行
```
$python CheckList.py
```
当ansible.log中返回的值均为ip=>success时说明对应服务器环境可用。

