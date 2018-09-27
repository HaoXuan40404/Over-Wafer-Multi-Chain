# 多链操作手册

## 部署物料包
$git clone https://github.com/ywy2090/multi-chain.git
cd multi-chain
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
多链物料包结构如上述所示，相关操作会在对应命令中进行解释

## 查询命令 -h
```
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
```
以上是物料包支持的相关操作，结束如下。

## 生成多链安装包 --build命令
本命令是解析用户输入的conf文件，生成相应安装包的命令。用户使用前需要确保运维服务器可以启动1.3版本的fisco-bcos，并且对应服务器的环境可以启动fisco-bcos

### 生成单条链
命令有两个input参数，分别为conf配置和fisco-bcos路径，示例如下
```
$python main.py --build ./conf/sample_12345_v1.0.conf $PATH/fisco-bcos
```
如果要生成某一条的链安装包执行第一个命令，如果在该目录下有多个安装包的conf文件，则执行第二条命令。build命令第二项参数为fisco-bcos的路径

mchain.conf为相关的部署目录和机构名称，用户根据需要修改。

用户使用时，首先更改./conf 目录下的sample_12345_v1.0.conf文件，如果需要部署多条链，需要拷贝多个conf文件。sample_12345_v1.0.conf文件示例如下：
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
  
然后在127.0.0.1服务器上启动3个节点, 按照默认的配置：

* 第1个节点的端口：p2p 30303、rpc 8545、channel 8821
* 第2个节点的端口：p2p 30304、rpc 8546、channel 8822
* 第3个节点的端口：p2p 30305、rpc 8547、channel 8823
  
上述配置共同在两个服务器上组成6个节点的一条链。

生成的安装包在./data/chain 目录下


### 生成多条链
用户在conf文件夹下配置多个.conf文件，如sample_12345_v1.0.conf，sample_12346_v1.0.conf,sample_12347_v1.0.conf
配置分别为
#### sample_12345_v1.0.conf
```
;common config
[chain]
chainid=12345
version=v1.0.0

;port config, in general, use the default values
[ports]
; p2p port
p2p_port=30303
; rpc port
rpc_port=8545
; channel port
channel_port=8821

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
####  sample_12346_v1.0.conf
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
node0=127.0.0.2 127.0.0.2 2
node1=127.0.0.3 127.0.0.3 2
node2=127.0.0.4 127.0.0.4 2
```
####  sample_12347_v1.0.conf
```
;common config
[chain]
chainid=12347
version=v1.0.0

;port config, in general, use the default values
[ports]
; p2p port
p2p_port=30303
; rpc port
rpc_port=8545
; channel port
channel_port=8821

;node info
[nodes]
; node config format : nodeIDX= host_ip p2p_ip node_num
; IDX is index value
; host_ip : host ip network of the server
; p2p_ip ：p2p ip network of the server
; num ：the num of the node on this server
node0=127.0.0.5 127.0.0.5 2
node1=127.0.0.6 127.0.0.6 3
```
执行
```
$python main.py --build ./conf $PATH/fisco-bcos
```
上面的配置会生成三条链，
链id12345的链会在
首先要在127.0.0.1服务器上启动3个节点, 按照默认的配置：

* 第1个节点的端口：p2p 30303、rpc 8545、channel 8821
* 第2个节点的端口：p2p 30304、rpc 8546、channel 8822
* 第3个节点的端口：p2p 30305、rpc 8547、channel 8823
  
然后在127.0.0.1服务器上启动3个节点, 按照默认的配置：

* 第1个节点的端口：p2p 30303、rpc 8545、channel 8821
* 第2个节点的端口：p2p 30304、rpc 8546、channel 8822
* 第3个节点的端口：p2p 30305、rpc 8547、channel 8823

  
组成6个节点的一条链。

链id12346的链会在
首先要在127.0.0.2服务器上启动2个节点, 按照默认的配置：

* 第1个节点的端口：p2p 30343、rpc 8555、channel 8831
* 第2个节点的端口：p2p 30344、rpc 8556、channel 8832
  
然后在127.0.0.3服务器上启动2个节点, 按照默认的配置：

* 第1个节点的端口：p2p 30343、rpc 8555、channel 8831
* 第2个节点的端口：p2p 30344、rpc 8556、channel 8832
  
最后在127.0.0.4服务器上启动2个节点, 按照默认的配置：

* 第1个节点的端口：p2p 30343、rpc 8555、channel 8831
* 第2个节点的端口：p2p 30344、rpc 8556、channel 8832
* 
组成6个节点的一条链。

链id12347的链同理会在127.0.0.5和127.0.0.6上共同生成5个节点组成的一条链

## 网络环境测试 --echo命令
echo命令用来测试运维服务器是否可以与配置好的所有服务器进行ansible通信，操作如下
```
python main.py --echo all or host_ip or [host_ip1 host_ip2 ...]
```
检测ansible配置的所有服务器是否可以进行通信
示例：
### 测试所有配置服务器
```
python main.py --echo all
```
正确会得到以下提示
```
INFO |  echo opr begin.
INFO |  ansible echo opr success, host is all.
INFO |  echo opr end.
```
### 测试单个服务器
```
python main.py --echo 127.0.0.1
```
正确会得到以下提示
```
INFO |  echo opr begin.
INFO |  ansible echo opr success, host is 127.0.0.1.
INFO |  echo opr end.
```
### 测试多个服务器
```
python main.py --echo 127.0.0.1 127.0.0.2 127.0.0.3
```
正确会得到以下提示
```
INFO |  echo opr begin.
INFO |  ansible echo opr success, host is 127.0.0.1.
INFO |  ansible echo opr success, host is 127.0.0.2.
INFO |  ansible echo opr success, host is 127.0.0.3.
INFO |  echo opr end.
```



## 发布多链安装包 --publish命令
publish为多链的发布命令，用户需要制定链id和版本号，中间用":"隔开
```
$python main.py --publish chain_id_1:version_1 chain_id_2:version_2 ...
```
chain_id_n:version_n 为chain的id和版本号，中间用":"隔开
示例：
用户需要推上面生成的链版本号为12345,12346,12347的链。

执行:
```
$python main.py --publish 12345:v1.0.0 12346:v1.0.0 12347:v1.0.0
```
执行完成后可以看到
```
INFO |  publish opr begin.
****
****
INFO |  publish opr end.
```

## 启动多链节点 --start命令
start命令允许用户在运维服务器上启动所有节点，或者某条链的节点，或者某条链对应某个服务器的节点。
```
$python main.py --start [all or chain_id or chain_id:host_ip]
```

三种参数分别对应启动部署的所有链的节点，部署的对应chain_id链的节点，和对应chain_id的host_ip的服务器的节点
### 启动部署所有链所有节点
```
$python main.py --start all
```
执行完成后可以看到
```
INFO |  start opr begin.
INFO |  ansible start opr success, host is 127.0.0.1.
INFO |  ansible start opr success, host is 127.0.0.2.
***
***
INFO |  start opr end.
```
上述命令启动了部署完成的所有链的全部节点
### 启动多条链节点
```
$python main.py --start 12345 12346 12347
```
执行完成后可以看到
```
INFO |  start opr begin.
INFO |  ansible start opr success, host is 127.0.0.1.
INFO |  ansible start opr success, host is 127.0.0.2.
***
***
INFO |  start opr end.
```
上述命令启动了链id为12345 12346 12347三条链的节点

### 启动多条链对应服务器节点
```
$python main.py --start 12345:127.0.0.1 12346:127.0.0.2 12347:127.0.0.3
```
执行完成后可以看到
```
INFO |  start opr begin.
INFO |  ansible start opr success, host is 127.0.0.1.
INFO |  ansible start opr success, host is 127.0.0.2.
***
***
INFO |  start opr end.
```
上述命令启动了链12345在127.0.0.1服务器上的3个节点， 链12346在127.0.0.2上的3个节点， 12347在127.0.0.3上的2个节点。

## 停止多链节点 --stop命令
```
$python main.py --stop [all or chain_id or chain_id:host_ip]
```
stop命令的原理与start命令类似
示例如下：
### 停止部署所有链所有节点
```
$python main.py --stop all
```

上述命令停止了部署完成的所有链的全部节点
### 停止多条链节点
```
$python main.py --stop 12345 12346 12347
```

上述命令启动了链id为12345 12346 12347三条链的节点

### 停止多条链对应服务器节点
```
$python main.py --stop 12345:127.0.0.1 12346:127.0.0.2 12347:127.0.0.3
```
上述命令停止了链12345在127.0.0.1服务器上的3个节点， 链12346在127.0.0.2上的3个节点， 12347在127.0.0.3上的2个节点。

## 检查多链节点启动情况 --check命令
```
$python main.py --check [all or chain_id or chain_id:host_ip]
```
check命令的原理与start命令类似
示例如下：
### 检查部署所有链所有节点
```
$python main.py --check all
```

### 检查多条链节点
```
$python main.py --check 12345 12346 12347
```

### 检查多条链对应服务器节点
```
$python main.py --check 12345:127.0.0.1 12346:127.0.0.2 12347:127.0.0.3
```

## 检查多链节点运行情况 --monitor命令
```
$python main.py --monitor [all or chain_id or chain_id:host_ip]
```
monitor命令的原理与start命令类似
示例如下：
### 检查部署所有链所有节点
```
$python main.py --monitor all
```

### 检查多条链节点
```
$python main.py --monitor 12345 12346 12347
```

### 检查多条链对应服务器节点
```
$python main.py --monitor 12345:127.0.0.1 12346:127.0.0.2 12347:127.0.0.3
```

## **请注意 monitor命令是检查节点的运行状况，check命令是检查节点的启动情况**

## 列出生成安装包节点 --pkg_list命令
```
$python main.py --pkg_list [all or chain_id]
```
pkg_list命令的原理与start命令类似
示例如下：
### 列出所有节点
```
$python main.py --pkg_list all
```

### 列出多条链节点
```
$python main.py --pkg_list 12345 12346 12347
```


## 列出发布安装包节点 --pub_list命令
```
$python main.py --pub_list [all or chain_id]
```
ppub_list命令的原理与start命令类似
示例如下：
### 列出所有节点
```
$python main.py --pub_list all
```

### 列出多条链节点
```
$python main.py --pub_list 12345 12346 12347
```

## ca证书相关操作 
多链物料包允许用户生成相应证书，fisco bcos的证书相关介绍请参考-[证书介绍]()，操作如下

### 生成根证书 --chainca命令
用户可以指定目录，生成根证书
```
python main.py --chainca ./dir_chain_ca(SET)
```
执行完成后用户可以在指定文件夹下看到根证书ca.crt 和私钥ca.key 。
### 生成机构证书 --agencyca命令
用户可以指定机构证书目录，链证书存放目录和机构名称，生成机构证书
```
python main.py --agencyca ./dir_agency_ca(SET) ./chain_ca_dir The_Agency_Name
```
执行完成后可以在./dir_agency_ca(SET)路径下生成名为The_Agency_Name的文件夹，包含相应的机构证书

### 生成sdk证书 --sdkca
用户可以指定sdk存放目录，机构证书存放目录，生成sdk证书
sdkca ./dir_sdk_ca(SET) ./dir_agency_ca
执行完成后可以在./dir_sdk_ca(SET)路径下生成名为sdk的文件夹，包含相应的sdk证书