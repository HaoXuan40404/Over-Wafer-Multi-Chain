# 自主维护多链操作手册
OWMC允许用户在不依赖ansible的情况下自行维护多链生成的安装包，操作手册如下：

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
usage: main.py [-h] [--version] [--cainit] [-g]
               [--build ./config.conf or ./conf/ fisco_path]
               [--expand ./config.conf, dir ./config.conf, dir]
               [--export chain_id chain_version dest_path]
               [--pkglist all or chain_id [all or chain_id ...]]
               [--envcheck all or host_ip [all or host_ip ...]]
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

