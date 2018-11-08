# 多链操作手册

## 部署物料包
```
$ git clone https://github.com/HaoXuan40404/Over-Wafer-Multi-Chain.git
$ git checkout dev
```
### 安装OWMC
用户需要安装OWMC，执行时需要root权限，安装脚本相关参数如图所示：
```
./install.sh -h
Usage:
Optional:
    -d  <dir>           The dir of owmc will be install. (default: /usr/loca/)
    -p  <path>          The python path. (default: /usr/bin/python)
    -g                  Install guomi deps. (default: not install guomi deps.)
    -f                  Install owmc even if it has been installed.
    -h                  This help.
Example:
    bash install.sh
    bash install.sh -d /usr/local -p /usr/bin/python -f -g
```
- -d 命令 指定安装路径
  
OWMC默认安装在/usr/local路径下，-d命令会将OWMC安装在指定路径，
- -p 命令 指定python路径
  
-p命令将指定用户的python路径，OWMC默认依赖/usr/bin/python下的python，由于OWMC需要依赖python2.7或3.5以上版本，用户可以指定python路径
- -g 命令 国密环境初始化
  
-g命令会安装fisco bcos需要的国密依赖，使用国密版fisco bcos必须指定次命令
- -f 命令 强制从新安装OWMC
  
用户可以使用-f命令从新安装owmc
- -h 命令 帮助命令
  
-h命令会显示install脚本的帮助信息

示例：

如用户希望在/usr/local下安装国密版owmc，使用/usr/bin/python的python版本，执行：
```
$ bash install.sh -d /usr/local -p /usr/bin/python -f -g
```



## 文件介绍

### hosts配置
```
vim hosts.conf
```

用户conf文件夹下修改hosts.conf格式如下
```
username 127.0.0.1 36000 123
username 127.0.0.2 36000 123
username 127.0.0.3 36000 123
username 127.0.0.4 36000 123
username 127.0.0.5 36000 123
```
第一项为ssh通信用户名，第二项为目标服务器ip 第三项为ssh通信端口号，第四项为ssh通信的密码
### 修改链配置mchain.conf
```
vim mchain.conf
```

```
; 机构相关配置
[agent]
; 机构名称
agent_name=WB

[ansible]
; 部署目录
dir=/data/app
```
agent_name名称为机构名称，根据需要修改。

dir为用户推包时的对应文件夹，请确认用户有权限对该文件夹进行操作。

### 配置链的信息sample_12345_v1.0.conf
在本sample中，用户部署两条链，其中一条链id为12345，另外一条链id为12346，版本号均为v1.0.0
```
cp sample_12345_v1.0.conf sample_12346_v1.0.conf
```
修改第一条链的配置
```
vim sample_12345_v1.0.conf
```
<font color="#0099ff">修改sample_12345_v1.0.conf文件如下</font>
```
;common config
[chain]
chainid=12345
version=v1.0.0
```
链相关配置，chainid为链id，必须为整形。version为版本号
```
;port config, in general, use the default values
[ports]
; p2p port
p2p_port=30303
; rpc port
rpc_port=8545
; channel port
channel_port=8821
```
fisco-bcos的每个节点需要使用3个端口,p2pport、rpcport、channelport, [ports]配置的端口是服务器上面的第一个节点使用的端口,其他节点依次递增。
```
;node info
[nodes]
; node config format : nodeIDX= host_ip p2p_ip node_num
; IDX is index value
; host_ip : host ip network of the server
; p2p_ip ：p2p ip network of the server
; num ：the num of the node on this server
node0=127.0.0.1 127.0.0.1 3
node1=127.0.0.2 127.0.0.2 3
```

上面的配置首先要在127.0.0.1服务器上启动3个节点, 按照默认的配置：

* 第1个节点的端口：p2p 30303、rpc 8545、channel 8821
* 第2个节点的端口：p2p 30304、rpc 8546、channel 8822
* 第3个节点的端口：p2p 30305、rpc 8547、channel 8823
  
然后在127.0.0.2服务器上启动3个节点, 按照默认的配置：

* 第1个节点的端口：p2p 30303、rpc 8545、channel 8821
* 第2个节点的端口：p2p 30304、rpc 8546、channel 8822
* 第3个节点的端口：p2p 30305、rpc 8547、channel 8823
  
上述配置共同在两个服务器上组成6个节点的一条链。

生成的安装包在./data/chain 目录下

修改第二条链的配置
```
vim sample_12346_v1.0.conf
```
<font color="#0099ff">修改sample_12346_v1.0.conf文件如下</font>

```
;common config
[chain]
chainid=12346
version=v1.0.0

;port config, in general, use the default values
[ports]
; p2p port
p2p_port=30343
; rpc port
rpc_port=8555
; channel port
channel_port=8831

;node info
[nodes]
; node config format : nodeIDX= host_ip p2p_ip node_num
; IDX is index value
; host_ip : host ip network of the server
; p2p_ip ：p2p ip network of the server
; num ：the num of the node on this server
node0=127.0.0.1 127.0.0.1 2
node1=127.0.0.2 127.0.0.2 2
node2=127.0.0.3 127.0.0.3 2
```

首先要在127.0.0.1服务器上启动2个节点, 

* 第1个节点的端口：p2p 30343、rpc 8555、channel 8831
* 第2个节点的端口：p2p 30344、rpc 8556、channel 8832
  
然后在127.0.0.2服务器上启动2个节点, 按照默认的配置：

* 第1个节点的端口：p2p 30343、rpc 8555、channel 8831
* 第2个节点的端口：p2p 30344、rpc 8556、channel 8832
  
最后在127.0.0.3服务器上启动2个节点, 按照默认的配置：

* 第1个节点的端口：p2p 30343、rpc 8555、channel 8831
* 第2个节点的端口：p2p 30344、rpc 8556、channel 8832


# 初始化命令
用户执行安装命令后，可以使用owmc的相关操作，功能介绍如下

## 查询命令 -h
```
owmc -h
```
可以查询到相关的操作命令
```
owmc -h
usage: owmc [-h] [--version] [--ansibleinit  hosts config file] [--cainit]
            [--build ./config.conf or ./conf/ fisco_path]
            [--expand ./config.conf, dir ./config.conf, dir]
            [--export chain_id chain_version dest_path]
            [--pkglist all or chain_id [all or chain_id ...]] [--direct]
            [--publish chain_id:version [chain_id:version ...]]
            [--start all or chain_id or [chain_id:host_ip ...]]
            [--stop all or chain_id or [chain_id:host_ip ...]]
            [--register chain_id  host_ip node]
            [--unregister chain_id  host_ip node]
            [--diagnose all or chain_id or [chain_id:host_ip ...]]
            [--check all or chain_id or [chain_id:host_ip ...]]
            [--publist all or chain_id or [all or chain_id or ...]]
            [--lshost host_ip [host_ip ...]] [--force]
            [--telnet 'all' or host_ip or chain_id ['all' or host_ip or chain_id ...]]
            [--envcheck all or host_ip [all or host_ip ...]]
            [--docmd  host ip or chain id or 'all' shell cmd or shell file, eg ： 'ls -lt'?test.sh]
            [--pushfile host ip or chain id or 'all' file or dir to be push. dst dir.]
            [--chainca chain_dir]
            [--agencyca agency_dir chain_dir  agency_name]
            [--nodeca agency_dir node _dir node_name]
            [--sdkca sdk_dir agency_dir] [--gm]

```
以上是物料包支持的相关操作，解释如下。

## 查看多链物料包版本 --help命令

## 查看多链物料包版本 --version命令
本命令用于查看当前多链物料包版本
```
$ owmc --version
or
$ owmc -v
```
会得到如下提示
```
INFO | v1.1.0
```

## 初始化ansible --init命令
用户在配置conf/hosts时，需要用到本命令。

本命令需要sudo权限对ansible的配置进行修改，用户每次修改hosts.conf都需要运行本命令。

```
$ python main.py --init
```
会得到如下提示
```
INFO | ansible init success
```
**注意，用户如果需要修改主机配置，则每次修改完./conf/hosts.conf后都需要执行init_ansible命令**

用户可以指定参数all查询配置的所有服务器，或是指定某些服务器ip查询对应服务器依赖。

## 初始化机构证书命令 --cainit命令
物理多链默认mchain.conf配置中的的机构名称为WB，并且在ca目录下已经存储了WB的的国密与非国密版的证书。当用户希望用其他机构的证书生成或扩容区块链之前，需要先使用本命令进行证书初始化。

注意，用户需要提供需要的对应机构的证书。(可以参考证书生成命令)

```
$ owmc --cainit ./cert_path
```
./cert_path为用户指定的证书文件夹，证书文件夹下应该包含链证书，机构文件夹包含机构证书和包含sdk证书的sdk文件夹，示例如下：

```
.
├── ca.crt
├── ca.key
└── WB
    ├── agency.crt
    ├── agency.csr
    ├── agency.key
    ├── agency.srl
    ├── ca-agency.crt
    ├── ca.crt
    ├── cert.cnf
    └── sdk
        ├── ca.crt
        └── client.keystore
或是
.
├── gmca.crt
├── gmca.key
├── gmca.srl
├── gmsm2.param
└── WB
    ├── gmagency.crt
    ├── gmagency.key
    ├── gmca.crt
    ├── gmsm2.param
    └── sdk
        ├── ca.crt
        ├── ca.key
        ├── cert.cnf
        ├── client.keystore
        ├── server.crt
        └── server.key
```
本命令同时支持国密证书和非国密证书的初始化。

**注意，用户如果需要修改主机配置，则每次修改完./conf/hosts.conf后都需要执行init_ansible命令**

用户可以指定参数all查询配置的所有服务器，或是指定某些服务器ip查询对应服务器依赖。

# 安装包操作命令



## 生成多链安装包 --build命令
本命令是解析用户输入的conf文件，生成相应安装包的命令。用户使用前需要确保运维服务器可以启动1.3版本的fisco-bcos，并且对应服务器的环境可以启动fisco-bcos,根据用户指定的fisco-bcos版本，可以生成国密或非国密的链，目前支持1.3版本的fisco-bcos。

*** 注意，如果用户需要修改机构名称，需要先执行cainit命令，初始化需要机构的证书名称。 ***

*** 注意，如果用户需要生成国密安装包，需要在安装时加上-g命令，安装国密证书库（只需要在运维服务器上安装即可） ***

### 生成单条链
命令有两个input参数，分别为conf配置和fisco-bcos路径，示例如下
```
$ owmc --build ./conf/sample_12345_v1.0.conf $PATH/fisco-bcos
```
如果要生成某一条的链安装包执行第一个命令，如果在该目录下有多个安装包的conf文件，则执行第二条命令。build命令第二项参数为fisco-bcos的路径

mchain.conf为相关的部署目录和机构名称，用户根据需要修改。

用户使用时，首先更改./conf 目录下的sample_12345_v1.0.conf文件，如果需要部署多条链，需要拷贝多个conf文件。

执行
```
$ owmc --build ./chain $PATH/fisco-bcos
```
可以生成chain文件夹下配置的多条链

## 生成扩容安装包 --expand命令
本命令是解析用户输入的conf文件，生成相应扩容安装包的命令。用户使用前需要确保运维服务器可以启动1.3版本的fisco-bcos，并且对应服务器的环境可以启动fisco-bcos。

用户在进行扩容操作时，需要配置conf.conf文件，若是在运维服务器上生成安装包，则只需要驶入conf文件，如果是不同机构间库容弄，需要输入conf文件和包含给定需要扩容链的 genesis.json，节点启动需要的bootstapnodes.json, 和fisco-bcos可执行文件的文件夹。

命令执行成功之后会在data文件夹下生成扩容安装包

执行
```
同机构扩容，在原有运维服务器上
$ owmc --expand ./config.conf .
异机构见扩容，或是同机构在非原有运维服务器上扩容，
$ owmc -expand ./config.conf ./dir_path
```
第一项为扩容配置文件，第二项dir_path内包含fisco-bcos二进制文件路径，需要扩容的链的genesis.json文件，需要扩容的链的bootstapnodes.json文件

*** 请确保不要让国密和非国密的fisco-bcos互联 ***


## 导出安装包命令 --export命令
OWMC支持用户导出安装包，自行管理和配置多链。

执行
```
$ owmc --export chain_id version $export_path/
```
如用户希望把chain id为12345，版本号为v1.0.0的安装包导出到mydata文件夹，则执行
```
$ owmc --export 12345 v1.0.0  /mydata/
```
执行成功后会在mydata文件夹下导出链12345 版本号为v1.0.0下对应hostip的安装包，如
```
127.0.0.1 127.0.0.2 127.0.0.3
```
用户将这些安装包推送至指定服务器，启动节点。


## 列出生成安装包节点 --pkglist命令
```
$ owmc --pkglist [all or chain_id]
```
pkglist命令的原理与start命令类似

使用此命令可以查看所有生成安装包链信息，节点信息，占用端口信息等。
示例如下：
### 列出所有节点
```
$ owmc --pkglist all
```

### 列出多条链节点
```
$ owmc --pkglist 12345 12346 12347
```

## 强制导出命令 --direct
此命令需要与export命令联合使用，为了应对不同机构之间的需求，export时采用此命令，OWMC将会直接将安装包导出，导出的所有安装包形式上都会一直，不会进行负载均衡处理。
```
$ owmc --export chain_id version $export_path/ --direct
```

# 多链管理工具

*** 本部分命令依赖ansible ***

## 发布多链安装包 --publish命令
在用户推送安装包之前，建议首先检查目标服务器环境依赖，推荐使用--envcheck命令进行检测。

publish为多链的发布命令，用户需要制定链id和版本号，中间用":"隔开
```
$ owmc --publish chain_id_1:version_1 chain_id_2:version_2 ...
```
chain_id_n:version_n 为chain的id和版本号，中间用":"隔开
示例：
用户需要推上面生成的链版本号为12345,12346,12347的链。

执行:
```
$ owmc --publish 12345:v1.0.0 12346:v1.0.0 12347:v1.0.0
```
执行完成后可以看到
```
INFO |  publish begin.
****
****
INFO |  publish end.
```

## 启动多链节点 --start命令
start命令允许用户在运维服务器上启动所有节点，或者某条链的节点，或者某条链对应某个服务器的节点。
```
$ owmc --start [all or chain_id or chain_id:host_ip]
```

三种参数分别对应启动部署的所有链的节点，部署的对应chain_id链的节点，和对应chain_id的host_ip的服务器的节点
### 启动部署所有链所有节点
```
$ owmc --start all
```
执行完成后可以看到
```
INFO |  start begin.
INFO |  ansible start success, host is 127.0.0.1.
INFO |  ansible start success, host is 127.0.0.2.
***
***
INFO |  start end.
```
上述命令启动了部署完成的所有链的全部节点
### 启动多条链节点
```
$ owmc --start 12345 12346 12347
```
执行完成后可以看到
```
INFO |  start begin.
INFO |  ansible start success, host is 127.0.0.1.
INFO |  ansible start success, host is 127.0.0.2.
***
***
INFO |  start end.
```
上述命令启动了链id为12345 12346 12347三条链的节点

### 启动多条链对应服务器节点
```
$ owmc --start 12345:127.0.0.1 12346:127.0.0.2 12347:127.0.0.3
```
执行完成后可以看到
```
INFO |  start begin.
INFO |  ansible start success, host is 127.0.0.1.
INFO |  ansible start success, host is 127.0.0.2.
***
***
INFO |  start end.
```
上述命令启动了链12345在127.0.0.1服务器上的3个节点， 链12346在127.0.0.2上的3个节点， 12347在127.0.0.3上的2个节点。

## 停止多链节点 --stop命令
```
$ owmc --stop [all or chain_id or chain_id:host_ip]
```
stop命令的原理与start命令类似，示例如下：
### 停止部署所有链所有节点
```
$ owmc --stop all
```

上述命令停止了部署完成的所有链的全部节点
### 停止多条链节点
```
$ owmc --stop 12345 12346 12347
```

上述命令启动了链id为12345 12346 12347三条链的节点

### 停止多条链对应服务器节点
```
$ owmc --stop 12345:127.0.0.1 12346:127.0.0.2 12347:127.0.0.3
```
上述命令停止了链12345在127.0.0.1服务器上的3个节点， 链12346在127.0.0.2上的3个节点， 12347在127.0.0.3上的2个节点。

## 注册观察节点入网命令 --register 
```
$ owmc --register chain_id  host_ip node
```
用户输入链id，对应的hospip，以及节点序号，将观察节点加入共识列表，变为记账节点。
示例如下：
```
$ owmc --register 12345  127.0.0.1 node3
```

## 踢出记账节点命令 --unregister 
```
$ owmc --unregister chain_id  host_ip node
```
用户输入链id，对应的hospip，以及节点序号，将记账踢出共识列表，变为观察节点。
示例如下：
```
$ owmc --unregister 12345  127.0.0.1 node3
```

## 诊断多链节点运行情况 --diagnose
```
$ owmc --diagnose [all or chain_id or chain_id:host_ip]
```
diagnose命令的原理与start命令类似

示例如下：
### 检查部署所有链所有节点
```
$ owmc --diagnose all
```

### 检查多条链节点
```
$ owmc --diagnose 12345 12346 12347
```

### 检查多条链对应服务器节点
```
$ owmc --diagnose 12345:127.0.0.1 12346:127.0.0.2 12347:127.0.0.3
```

## 检查多链节点启动情况 --check命令
```
$ owmc --check [all or chain_id or chain_id:host_ip]
```
check命令会检查节点的运行情况，并返回链的基本状态，如块高，共识节点数等。

check命令的原理与start命令类似
示例如下：
### 检查部署所有链所有节点
```
$ owmc --check all
```

### 检查多条链节点
```
$ owmc --check 12345 12346 12347
```

### 检查多条链对应服务器节点
```
$ owmc --check 12345:127.0.0.1 12346:127.0.0.2 12347:127.0.0.3
```


## 检查目标服务器环境依赖 --envcheck命令
本命令可以检测目标服务器环境依赖是否满足，当运维服务器生成安装包后，建议用户在推送安装包之前首先检测目标服务器环境

```
$ owmc --envcheck all  or host_ip ...
```
运行此命令之后会检查对应服务器是否满足运行fisco bcos的要求


## 列出发布安装包节点 --publist命令
```
$ owmc --publist [all or chain_id]
```
ppublist命令的原理与start命令类似

使用此命令可以查看所有发布后的安装包链信息，节点信息，占用端口信息等。
示例如下：
### 列出所有节点
```
$ owmc --publist all
```

### 列出多条链节点
```
$ owmc --publist 12345 12346 12347
```

## 检查发布后对应服务器端口占用情况 --lshost命令
```
$ owmc --ls_host hostip
```
使用本命令可以观察对用服务器上发布后安装包占用的端口情况


# 其他工具命令

## 网络环境测试 --telnet命令
telnet命令用来测试运维服务器是否可以与配置好的所有服务器进行ansible通信，操作如下
```
$ owmc --telnet all or host_ip or [host_ip1 host_ip2 ...]
```
检测ansible配置的所有服务器是否可以进行通信
示例：
### 测试所有配置服务器
```
$ owmc --telnet all
```
正确会得到以下提示
```
INFO |  telnet begin.
INFO |  ansible telnet success, host is all.
INFO |  telnet end.
```
### 测试单个服务器
```
$ owmc --telnet 127.0.0.1
```
正确会得到以下提示
```
INFO |  telnet  begin.
INFO |  ansible telnet success, host is 127.0.0.1.
INFO |  telnet end.
```
### 测试多个服务器
```
$ owmc --telnet 127.0.0.1 127.0.0.2 127.0.0.3
```
正确会得到以下提示
```
INFO |  telnet begin.
INFO |  ansible telnet success, host is 127.0.0.1.
INFO |  ansible telnet success, host is 127.0.0.2.
INFO |  ansible telnet success, host is 127.0.0.3.
INFO |  telnet end.
```


## 组合命令 --gm 国密命令相关
--gm命令只能和证书生成命令组合使用，使用前请确保在安装owmc时安装了国密版本

fisco bcos支持用户提前生成需要的节点证书，用户需要在目录下按照文档说明结构存放所有的节点证书，存放结构为
chainID/version/hostip/node_index/
如12345/v1.0.0/127.0.0.1/node0/
需要存放
ca.crt agency.crt node.key node.pubkey node.crt

用户在使用build命令时，可以组合--gm命令，指定证书路径生成多链。
```
$ owmc --chainca ./dir_chain_ca(SET) --gm
```
执行安装后会生成国密版本的证书



## 执行shell命令或shell脚本 --docmd命令
cmd_push命令允许用户批量在对应服务器上执行本地的脚本，或是在对应服务器上直接执行shell命令
```
$ owmc --docmd all:"cmd_1 cmd_2" or chain_id:"cmd_1 cmd_2" or all:"./test.sh"
```

执行时命令会检测本地是否有对应路径下的脚本文件，如果没有会去对应服务器执行，示例如下：

用户本地在mydata文件夹下编写了脚本script.sh, 在链12345对应的服务器上执行
```
$ owmc --docmd  12345:"/mydata/script.sh"
```
用户在链12345对应服务器的mydata文件夹下编写了脚本script.sh, 在对应的服务器上执行
```
$ owmc --docmd  12345:"bash /mydata/script.sh"
```
## 传输单独文件 --pushfile命令
push_file命令允许用户批量传输某个文件到对应服务器。
```
$ owmc --pushfile all:scr_path:dest_path or chain_id:scr_path:dest_path or \[chain_id:scr_path:dest_path or host_ip:scr_path:dest_path ...]]
```

命令中第一项是对应服务器或链参数

第二项为本地文件路径

第三项为对应服务器路径

注意本地路径和对应服务器路径格式一致，如都为绝对路径或相对路径

如用户希望将本地mydata文件夹下的ChangeLog.md推到链12345对应服务器的app文件夹，执行:
```
$ owmc --push_file 12345:/mydata/ChangeLog.md:/app/
```

## 组合命令 -f 强制推送安装包
-f命令只能与--publish/-p命令组合使用

publish命令在推送安装包时，会判断是否已经推送过，如果推送过就无法再次推送，-f命令会再次推送一次安装包。
如publish命令中的示例
```
$ owmc -p 12345:v1.0.0
```
由于链12345已经被推送过，因此推提示推送错误，此时执行：
```
$ owmc -p 12345:v1.0.0 -f
```
会讲链12345再次推送
## ca证书相关操作 
多链物料包允许用户生成相应证书，fisco bcos的证书相关介绍请参考-[证书介绍](https://fisco-bcos-documentation.readthedocs.io/zh_CN/feature-multichain/docs/usage/cert_permission.html)，操作如下

### 生成根证书 --chainca命令
用户可以指定目录，生成根证书
```
owmc --chainca ./dir_chain_ca(SET)
or
owmc --chainca ./dir_chain_ca(SET) --gm
```
执行完成后用户可以在指定文件夹下看到根证书ca.crt 和私钥ca.key。或者是国密版本的根证书gmca.crt 和私钥gmca.key。
### 生成机构证书 --agencyca命令
用户可以指定机构证书目录，链证书存放目录和机构名称，生成机构证书
```
owmc --agencyca ./dir_agency_ca(SET) ./chain_ca_dir The_Agency_Name
or
owmc --agencyca ./dir_agency_ca(SET) ./chain_ca_dir The_Agency_Name --gm
```
执行完成后可以在./dir_agency_ca(SET)路径下生成名为The_Agency_Name的文件夹，包含相应的机构证书

### 生成sdk证书 --sdkca
用户可以指定sdk存放目录，机构证书存放目录，生成sdk证书
```
owmc --sdkca ./dir_sdk_ca(SET) ./dir_agency_ca
or
owmc --sdkca ./dir_sdk_ca(SET) ./dir_agency_ca --gm
```
执行完成后可以在./dir_sdk_ca(SET)路径下生成名为sdk的文件夹，包含相应的sdk证书

### 生成节点证书 --nodeca
用户可以指定机构证书目录，节点存放目录和节点名称，生成节点证书
```
owmc --nodeca ./agency_dir node_dir(SET) node_name
or 
owmc --nodeca ./agency_dir node_dir(SET) node_name --gm
```
执行完成后可以在node_dir(SET) 路径下生成节点证书

