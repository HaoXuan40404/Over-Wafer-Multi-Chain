# 自主维护多链操作手册
OWMC允许用户在不依赖ansible的情况下自行维护多链生成的安装包，操作手册如下：

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

# 初始化命令
当用户没有配置ansible时，可以使用owmc的如下功能
## 查询命令 -h
```
$ owmc -h
```
可以查询到相关的操作命令
```
owmc -h
usage: owmc [-h] [--version] [--ansibleinit  hosts config file] [--cainit]
            [--build ./config.conf or ./conf/ fisco_path]
            [--expand ./config.conf, dir ./config.conf, dir]
            [--export chain_id chain_version dest_path]
            [--pkglist all or chain_id [all or chain_id ...]] [--direct]
            [--chainca chain_dir]
            [--agencyca agency_dir chain_dir  agency_name]
            [--nodeca agency_dir node _dir node_name]
            [--sdkca sdk_dir agency_dir] [--gm]
```
以上是物料包支持的相关操作，解释如下。


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

## 初始化机构证书命令 --cainit命令
物理多链默认mchain.conf配置中的的机构名称为FISCO，并且在ca目录下已经存储了FISCO的的国密与非国密版的证书。当用户希望用其他机构的证书生成或扩容区块链之前，需要先使用本命令进行证书初始化。

注意，用户需要提供需要的对应机构的证书。(可以参考证书生成命令)

```
$ owmc --cainit ./cert_path
```
./cert_path为用户指定的证书文件夹，证书文件夹下应该包含链证书，机构文件夹包含机构证书和包含sdk证书的sdk文件夹，示例如下：

```
.
├── ca.crt
├── ca.key
└── FISCO
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
└── FISCO
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

## 国密依赖安装脚本 install_tassl.sh

如果用户想要生成国密版fisco-bcos链，或是生成国密版证书，需要在运维服务器上执行国密依赖安装脚本。

操作如下：
```
$ cd ./scripts/ca/gm
$ ./install_tassl.sh
$ cd -
```
整个命令执行过程根据网速和cpu处理速度不同，时间会在1~5分钟。

# 安装包操作命令

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
agent_name=FISCO

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

## 生成多链安装包 --build命令
本命令是解析用户输入的conf文件，生成相应安装包的命令。用户使用前需要确保运维服务器可以启动1.3版本的fisco-bcos，并且对应服务器的环境可以启动fisco-bcos,根据用户指定的fisco-bcos版本，可以生成国密或非国密的链，目前支持1.3版本的fisco-bcos。

*** 注意，如果用户需要修改机构名称，需要先执行cainit命令，初始化需要机构的证书名称。 ***

*** 注意，如果用户需要生成国密安装包，需要先执行install_tassl.sh脚本，安装国密证书库（只需要在运维服务器上安装即可） ***


### 生成单条链
命令有两个input参数，分别为conf配置和fisco-bcos路径，示例如下
```
$ owmc --build ./sample_12345_v1.0.conf $PATH/fisco-bcos
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

# 多链管理命令


## 发布安装包 
用户使用export导出安装包之后，会在对应路径下生成多个名为hostip的安装包，用户需要手动将这些安装包推送到对应hostip的服务器上

## 启动多链节点
生成的安装包下拥有start.sh脚本可以启动该安装包下的所有节点，每个节点下同时有控制自己启动的start.sh脚本
### 启动所有节点
在对应服务器下，进入推送后的安装包，设安装包推送路径为./mydata
```
$ cd ./mydata
$ bash ./start.sh node0
```

### 启动某个节点
在对应服务器下，进入推送后的安装包，设安装包推送路径为./mydata
```
$ cd ./mydata
$ bash ./start.sh node0
```
或是
```
$ cd ./mydata/node0
$ bash ./start.sh
```

## 停止多链节点
生成的安装包下拥有stop.sh脚本可以停止该安装包下的所有节点，每个节点下同时有控制自己停止的stop.sh脚本

### 停止所有节点
在对应服务器下，进入推送后的安装包，设改路径为./mydata
```
$ cd ./mydata
$ bash ./stop.sh node0
```

### 停止某个节点
在对应服务器下，进入推送后的安装包，设安装包推送路径为./mydata
```
$ cd ./mydata
$ bash ./stop.sh node0
```
或是
```
$ cd ./mydata/node0
$ bash ./stop.sh
```

## 注册观察节点入网
生成的安装包下拥有register.sh脚本可以注册节点入网，设安装包推送路径为./mydata

用户输入节点序号，将观察节点node0加入共识列表，变为记账节点。

示例如下：
```
$ cd ./mydata
$ bash ./register.sh node0
```

## 踢出记账节点
生成的安装包下拥有unregister.sh脚本可以踢出记账节点，设安装包推送路径为./mydata

用户输入节点序号，将记账节点node0踢出共识列表，变为记账节点。

示例如下：
```
$ cd ./mydata
$ bash ./unregister.sh node0
```

## 诊断节点运行情况
生成的安装包下拥有diagnose.sh诊断节点运行情况，设安装包推送路径为./mydata

示例如下：
```
$ cd ./mydata
$ bash ./diagnose.sh
```

## 检查节点启动情况 --check命令
生成的安装包下拥有check.sh检查节点运行情况，设安装包推送路径为./mydata

示例如下：
```
$ cd ./mydata
$ bash ./check.sh
```

## 检查服务器环境依赖 --envcheck命令
本命令可以检测目标服务器环境依赖是否满足

生成的安装包下拥有deps_check.sh  deps_install.sh  os_check.sh 脚本分别可以检查操作环境，环境依赖和依赖安装，设安装包推送路径为./mydata

示例如下：
```
$ cd ./mydata/tools
$ bash ./os_check.sh
$ bash ./os_check.sh
$ bash ./deps_check.sh
$ bash ./deps_install.sh
```


# 其他工具命令


## 组合命令 --gm 国密命令相关
--gm命令只能和证书生成命令组合使用

fisco bcos支持用户提前生成需要的节点证书，用户需要在目录下按照文档说明结构存放所有的节点证书，存放结构为
chainID/version/hostip/node_index/
如12345/v1.0.0/127.0.0.1/node0/
需要存放
ca.crt agency.crt node.key node.pubkey node.crt

用户在使用build命令时，可以组合-gm命令，指定证书路径生成多链。
```
owmc --chainca ./dir_chain_ca(SET) -gm
```
执行安装后会生成国密版本的证书


## ca证书相关操作 
多链物料包允许用户生成相应证书，fisco bcos的证书相关介绍请参考-[证书介绍](https://fisco-bcos-documentation.readthedocs.io/zh_CN/feature-multichain/docs/usage/cert_permission.html)，操作如下

### 生成根证书 --chainca命令
用户可以指定目录，生成根证书
```
owmc --chainca ./dir_chain_ca(SET)
or
owmc --chainca ./dir_chain_ca(SET) -gm
```
执行完成后用户可以在指定文件夹下看到根证书ca.crt 和私钥ca.key。或者是国密版本的根证书gmca.crt 和私钥gmca.key。
### 生成机构证书 --agencyca命令
用户可以指定机构证书目录，链证书存放目录和机构名称，生成机构证书
```
owmc --agencyca ./dir_agency_ca(SET) ./chain_ca_dir The_Agency_Name
or
owmc --agencyca ./dir_agency_ca(SET) ./chain_ca_dir The_Agency_Name -gm
```
执行完成后可以在./dir_agency_ca(SET)路径下生成名为The_Agency_Name的文件夹，包含相应的机构证书

### 生成sdk证书 --sdkca
用户可以指定sdk存放目录，机构证书存放目录，生成sdk证书
```
owmc --sdkca ./dir_sdk_ca(SET) ./dir_agency_ca
or
owmc --sdkca ./dir_sdk_ca(SET) ./dir_agency_ca -gm
```
执行完成后可以在./dir_sdk_ca(SET)路径下生成名为sdk的文件夹，包含相应的sdk证书

### 生成节点证书 --nodeca
用户可以指定机构证书目录，节点存放目录和节点名称，生成节点证书
```
owmc --nodeca ./agency_dir node_dir(SET) node_name
or 
owmc --nodeca ./agency_dir node_dir(SET) node_name --gmm
```
执行完成后可以在node_dir(SET) 路径下生成节点证书

