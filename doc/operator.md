# 多链操作手册

## 部署物料包
```
$ git clone https://github.com/ywy2090/multi-chain.git
$ cd multi-chain
```
多链物料包结构如下所示，相关操作会在对应命令中进行解释
```
|-- conf
|-- data
|-- format.sh
|-- log
|-- main.py
|-- new.md
|-- pys
|-- README.md
|-- release_note.txt
|-- scripts
`-- tpl
```

# 初始化命令

## 查询命令 -h
```
python main.py -h
```
可以查询到相关的操作命令
```
usage: main.py [-h] [--version] [--init] [--cainit] [-g]
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
               [--lshost host_ip [host_ip ...]] [-f]
               [-t 'all' or host_ip or chain_id ['all' or host_ip or chain_id ...]]
               [--envcheck all or host_ip [all or host_ip ...]]
               [-d  host ip or chain id or 'all' shell cmd or shell file, eg ： 'ls -lt'、test.sh]
               [-P host ip or chain id or 'all' file or dir to be push. dst dir.]
               [--chainca chain ca dir to be generate.]
               [--agencyca agency ca dir to be generate. chain ca dir  agency name]
               [--nodeca agency ca dir node ca dir to be generate. node_name]
               [--sdkca sdk ca dir agency ca dir]
```
以上是物料包支持的相关操作，解释如下。

## 查看多链物料包版本 --help命令

## 查看多链物料包版本 -v --version命令
本命令用于查看当前多链物料包版本
```
$ python main.py --version
or
$ python main.py -v
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
or
$ python main.py -i
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
$ python main.py --cainit ./cert_path
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

## 生成多链安装包 --build命令
本命令是解析用户输入的conf文件，生成相应安装包的命令。用户使用前需要确保运维服务器可以启动1.3版本的fisco-bcos，并且对应服务器的环境可以启动fisco-bcos,根据用户指定的fisco-bcos版本，可以生成国密或非国密的链，目前支持1.3版本的fisco-bcos。

*** 注意，如果用户需要修改机构名称，需要先执行cainit命令，初始化需要机构的证书名称。 ***

*** 注意，如果用户需要生成国密安装包，需要先执行install_tassl.sh脚本，安装国密证书库（只需要在运维服务器上安装即可） ***


### 生成单条链
命令有两个input参数，分别为conf配置和fisco-bcos路径，示例如下
```
$ python main.py --build ./sample_12345_v1.0.conf $PATH/fisco-bcos
```
如果要生成某一条的链安装包执行第一个命令，如果在该目录下有多个安装包的conf文件，则执行第二条命令。build命令第二项参数为fisco-bcos的路径

mchain.conf为相关的部署目录和机构名称，用户根据需要修改。

用户使用时，首先更改./conf 目录下的sample_12345_v1.0.conf文件，如果需要部署多条链，需要拷贝多个conf文件。

执行
```
$ python main.py --build ./chain $PATH/fisco-bcos
```
可以生成chain文件夹下配置的多条链

## 生成扩容安装包 --expand命令
本命令是解析用户输入的conf文件，生成相应扩容安装包的命令。用户使用前需要确保运维服务器可以启动1.3版本的fisco-bcos，并且对应服务器的环境可以启动fisco-bcos。

用户在进行扩容操作时，需要配置conf.conf文件，若是在运维服务器上生成安装包，则只需要驶入conf文件，如果是不同机构间库容弄，需要输入conf文件和包含给定需要扩容链的 genesis.json，节点启动需要的bootstapnodes.json, 和fisco-bcos可执行文件的文件夹。

命令执行成功之后会在data文件夹下生成扩容安装包

执行
```
同机构扩容，在原有运维服务器上
$ python main.py --expand ./config.conf .
异机构见扩容，或是同机构在非原有运维服务器上扩容，
$ python main.py -expand ./config.conf ./dir_path
```
第一项为扩容配置文件，第二项dir_path内包含fisco-bcos二进制文件路径，需要扩容的链的genesis.json文件，需要扩容的链的bootstapnodes.json文件

*** 请确保不要让国密和非国密的fisco-bcos互联 ***


## 导出安装包命令 --export命令
OWMC支持用户导出安装包，自行管理和配置多链。

执行
```
$ python main.py --export chain_id version $export_path/
```
如用户希望把chain id为12345，版本号为v1.0.0的安装包导出到mydata文件夹，则执行
```
$ python main.py --export 12345 v1.0.0  /mydata/
```
执行成功后会在mydata文件夹下导出链12345 版本号为v1.0.0下对应hostip的安装包，如
```
127.0.0.1 127.0.0.2 127.0.0.3
```
用户将这些安装包推送至指定服务器，启动节点。


## 列出生成安装包节点 --pkglist命令
```
$ python main.py --pkglist [all or chain_id]
```
pkglist命令的原理与start命令类似

使用此命令可以查看所有生成安装包链信息，节点信息，占用端口信息等。
示例如下：
### 列出所有节点
```
$ python main.py --pkglist all
```

### 列出多条链节点
```
$ python main.py --pkglist 12345 12346 12347
```

## 强制导出命令 --direct
此命令需要与export命令联合使用，为了应对不同机构之间的需求，export时采用此命令，OWMC将会直接将安装包导出，导出的所有安装包形式上都会一直，不会进行负载均衡处理。
```
$ python main.py --export chain_id version $export_path/ --direct
```

# 多链管理工具
*** 本部分命令依赖ansible ***

## 发布多链安装包 --publish命令
publish为多链的发布命令，用户需要制定链id和版本号，中间用":"隔开
```
$ python main.py --publish chain_id_1:version_1 chain_id_2:version_2 ...
```
chain_id_n:version_n 为chain的id和版本号，中间用":"隔开
示例：
用户需要推上面生成的链版本号为12345,12346,12347的链。

执行:
```
$ python main.py --publish 12345:v1.0.0 12346:v1.0.0 12347:v1.0.0
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
$ python main.py --start [all or chain_id or chain_id:host_ip]
```

三种参数分别对应启动部署的所有链的节点，部署的对应chain_id链的节点，和对应chain_id的host_ip的服务器的节点
### 启动部署所有链所有节点
```
$ python main.py --start all
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
$ python main.py --start 12345 12346 12347
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
$ python main.py --start 12345:127.0.0.1 12346:127.0.0.2 12347:127.0.0.3
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
$ python main.py --stop [all or chain_id or chain_id:host_ip]
```
stop命令的原理与start命令类似，示例如下：
### 停止部署所有链所有节点
```
$ python main.py --stop all
```

上述命令停止了部署完成的所有链的全部节点
### 停止多条链节点
```
$ python main.py --stop 12345 12346 12347
```

上述命令启动了链id为12345 12346 12347三条链的节点

### 停止多条链对应服务器节点
```
$ python main.py --stop 12345:127.0.0.1 12346:127.0.0.2 12347:127.0.0.3
```
上述命令停止了链12345在127.0.0.1服务器上的3个节点， 链12346在127.0.0.2上的3个节点， 12347在127.0.0.3上的2个节点。

## 注册观察节点入网命令 --register 
```
$ python main.py --register chain_id  host_ip node
```
用户输入链id，对应的hospip，以及节点序号，将观察节点加入共识列表，变为记账节点。
示例如下：
```
$ python main.py --register 12345  127.0.0.1 node3
```

## 踢出记账节点命令 --unregister 
```
$ python main.py --unregister chain_id  host_ip node
```
用户输入链id，对应的hospip，以及节点序号，将记账踢出共识列表，变为观察节点。
示例如下：
```
$ python main.py --unregister 12345  127.0.0.1 node3
```

## 诊断多链节点运行情况 --diagnose
```
$ python main.py --diagnose [all or chain_id or chain_id:host_ip]
```
diagnose命令的原理与start命令类似

示例如下：
### 检查部署所有链所有节点
```
$ python main.py --diagnose all
```

### 检查多条链节点
```
$ python main.py --diagnose 12345 12346 12347
```

### 检查多条链对应服务器节点
```
$ python main.py --diagnose 12345:127.0.0.1 12346:127.0.0.2 12347:127.0.0.3
```

## 检查多链节点启动情况 --check命令
```
$ python main.py --check [all or chain_id or chain_id:host_ip]
```
check命令会检查节点的运行情况，并返回链的基本状态，如块高，共识节点数等。

check命令的原理与start命令类似
示例如下：
### 检查部署所有链所有节点
```
$ python main.py --check all
```

### 检查多条链节点
```
$ python main.py --check 12345 12346 12347
```

### 检查多条链对应服务器节点
```
$ python main.py --check 12345:127.0.0.1 12346:127.0.0.2 12347:127.0.0.3
```


## 检查目标服务器环境依赖 --envcheck命令
本命令可以检测目标服务器环境依赖是否满足

```
python main.py --envcheck all  or host_ip ...
```
运行此命令之后会检查对应服务器是否满足运行fisco bcos的要求


## 列出发布安装包节点 --publist命令
```
$ python main.py --publist [all or chain_id]
```
ppublist命令的原理与start命令类似

使用此命令可以查看所有发布后的安装包链信息，节点信息，占用端口信息等。
示例如下：
### 列出所有节点
```
$ python main.py --publist all
```

### 列出多条链节点
```
$ python main.py --publist 12345 12346 12347
```

## 检查发布后对应服务器端口占用情况 --lshost命令
```
$ python main.py --ls_host hostip
```
使用本命令可以观察对用服务器上发布后安装包占用的端口情况


# 其他工具命令

## 网络环境测试 -t --telnet命令
telnet命令用来测试运维服务器是否可以与配置好的所有服务器进行ansible通信，操作如下
```
$ python main.py -t all or host_ip or [host_ip1 host_ip2 ...]
```
检测ansible配置的所有服务器是否可以进行通信
示例：
### 测试所有配置服务器
```
$ python main.py -t all
```
正确会得到以下提示
```
INFO |  telnet begin.
INFO |  ansible telnet success, host is all.
INFO |  telnet end.
```
### 测试单个服务器
```
$ python main.py -t 127.0.0.1
```
正确会得到以下提示
```
INFO |  telnet  begin.
INFO |  ansible telnet success, host is 127.0.0.1.
INFO |  telnet end.
```
### 测试多个服务器
```
$ python main.py -t 127.0.0.1 127.0.0.2 127.0.0.3
```
正确会得到以下提示
```
INFO |  telnet begin.
INFO |  ansible telnet success, host is 127.0.0.1.
INFO |  ansible telnet success, host is 127.0.0.2.
INFO |  ansible telnet success, host is 127.0.0.3.
INFO |  telnet end.
```


## 组合命令 -g 国密命令相关
-g命令只能和证书生成命令组合使用

fisco bcos支持用户提前生成需要的节点证书，用户需要在目录下按照文档说明结构存放所有的节点证书，存放结构为
chainID/version/hostip/node_index/
如12345/v1.0.0/127.0.0.1/node0/
需要存放
ca.crt agency.crt node.key node.pubkey node.crt

用户在使用build命令时，可以组合-g命令，指定证书路径生成多链。
```
python main.py --chainca ./dir_chain_ca(SET) -g
```
执行安装后会生成国密版本的证书



## 执行shell命令或shell脚本 --docmd命令
cmd_push命令允许用户批量在对应服务器上执行本地的脚本，或是在对应服务器上直接执行shell命令
```
$ python main.py --docmd all:"cmd_1 cmd_2" or chain_id:"cmd_1 cmd_2" or all:"./test.sh"
```

执行时命令会检测本地是否有对应路径下的脚本文件，如果没有会去对应服务器执行，示例如下：

用户本地在mydata文件夹下编写了脚本script.sh, 在链12345对应的服务器上执行
```
$ python main.py --docmd  12345:"/mydata/script.sh"
```
用户在链12345对应服务器的mydata文件夹下编写了脚本script.sh, 在对应的服务器上执行
```
$ python main.py --docmd  12345:"bash /mydata/script.sh"
```
## 传输单独文件 --pushfile命令
push_file命令允许用户批量传输某个文件到对应服务器。
```
$ python main.py --pushfile all:scr_path:dest_path or chain_id:scr_path:dest_path or \[chain_id:scr_path:dest_path or host_ip:scr_path:dest_path ...]]
```

命令中第一项是对应服务器或链参数

第二项为本地文件路径

第三项为对应服务器路径

注意本地路径和对应服务器路径格式一致，如都为绝对路径或相对路径

如用户希望将本地mydata文件夹下的ChangeLog.md推到链12345对应服务器的app文件夹，执行:
```
$ python main.py --push_file 12345:/mydata/ChangeLog.md:/app/
```

## 组合命令 -f 强制推送安装包
-f命令只能与--publish/-p命令组合使用

publish命令在推送安装包时，会判断是否已经推送过，如果推送过就无法再次推送，-f命令会再次推送一次安装包。
如publish命令中的示例
```
$ python main.py -p 12345:v1.0.0
```
由于链12345已经被推送过，因此推提示推送错误，此时执行：
```
$ python main.py -p 12345:v1.0.0 -f
```
会讲链12345再次推送
## ca证书相关操作 
多链物料包允许用户生成相应证书，fisco bcos的证书相关介绍请参考-[证书介绍](https://fisco-bcos-documentation.readthedocs.io/zh_CN/feature-multichain/docs/usage/cert_permission.html)，操作如下

### 生成根证书 --chainca命令
用户可以指定目录，生成根证书
```
python main.py --chainca ./dir_chain_ca(SET)
or
python main.py --chainca ./dir_chain_ca(SET) -g
```
执行完成后用户可以在指定文件夹下看到根证书ca.crt 和私钥ca.key。或者是国密版本的根证书gmca.crt 和私钥gmca.key。
### 生成机构证书 --agencyca命令
用户可以指定机构证书目录，链证书存放目录和机构名称，生成机构证书
```
python main.py --agencyca ./dir_agency_ca(SET) ./chain_ca_dir The_Agency_Name
or
python main.py --agencyca ./dir_agency_ca(SET) ./chain_ca_dir The_Agency_Name -g
```
执行完成后可以在./dir_agency_ca(SET)路径下生成名为The_Agency_Name的文件夹，包含相应的机构证书

### 生成sdk证书 --sdkca
用户可以指定sdk存放目录，机构证书存放目录，生成sdk证书
```
python main.py --sdkca ./dir_sdk_ca(SET) ./dir_agency_ca
or
python main.py --sdkca ./dir_sdk_ca(SET) ./dir_agency_ca -g
```
执行完成后可以在./dir_sdk_ca(SET)路径下生成名为sdk的文件夹，包含相应的sdk证书

### 生成节点证书 --nodeca
用户可以指定机构证书目录，节点存放目录和节点名称，生成节点证书
```
python main.py --nodeca ./agency_dir node_dir(SET) node_name
or 
python main.py --nodeca ./agency_dir node_dir(SET) node_name -g
```
执行完成后可以在node_dir(SET) 路径下生成节点证书

