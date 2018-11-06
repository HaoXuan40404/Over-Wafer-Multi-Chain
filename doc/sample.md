# OWMC搭建示例
本章我们会给出一个示例，假设用户使用一台运维服务器，拥有三条托管服务器，hostip分别为127.0.0.1,127.0.0.2,127.0.0.3。让用户在运维服务器上快速搭建两条链，其中一条链有6个节点，分别部署在三台服务器上，另外一条链有4个节点，部署在自己的托管服务器上。



## 下载源码
```
git clone https://github.com/HaoXuan40404/Over-Wafer-Multi-Chain.git
git checkout dev
```

## 配置环境依赖

相关操作参考[环境依赖](https://fisco-bcos-documentation.readthedocs.io/zh_CN/feature-multichain/docs/mulchain/envcheck.html)

[JAVA配置](https://fisco-bcos-documentation.readthedocs.io/zh_CN/feature-multichain/docs/mulchain/javacheck.html)

[python配置](https://fisco-bcos-documentation.readthedocs.io/zh_CN/feature-multichain/docs/mulchain/pythoncheck.html)

[ansible配置](https://fisco-bcos-documentation.readthedocs.io/zh_CN/feature-multichain/docs/mulchain/ansiblecheck.html)

## 参数配置
在生成安装包之前，用户需要对hosts.conf，mchain.conf和sample_12345_v1.0.conf进行链相关属性配置
```
cd Over-Wafer-Multi-Chain/
cd conf/
```
### 修改hosts配置
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

## 启动两条链

### 初始化环境
```
python main.py --init
```
### 检查环境
```
python main.py --env_check all
```
### 生成安装包
假设用户的fisco-bcos程序放在/usr/local/bin/fisco-bcos。

tips，用户可以使用whereis fisco-bcos查找具体位置
```
$ python main.py --build ./conf /usr/local/bin/fisco-bcos
```
### 部署安装包
```
$ python main.py --publish 12345:v1.0.0 12346:v1.0.0
```
### 启动节点
```
$ python main.py --start all
```
### 检查节点启动情况
```
$ python main.py --check all
```
### 停止节点
```
$ python main.py --stop all
```
上述操作完成了两条链的搭建，更多操作请访问[操作手册](https://fisco-bcos-documentation.readthedocs.io/zh_CN/feature-multichain/docs/mulchain/operator.html)
