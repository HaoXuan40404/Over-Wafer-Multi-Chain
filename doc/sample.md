# OWMC搭建示例
本章我们会给出一个示例，假设用户使用一台运维服务器，拥有三条托管服务器，hostip分别为127.0.0.1,127.0.0.2,127.0.0.3。让用户在运维服务器上快速搭建一条链在127.0.0.1上有三个节点的区块链



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
第一项为ssh通信用户名，第二项为目标服务器ip 第三项为ssh通信端口号，第四项为ssh通信的密码，用户修改username 和密码为自己服务器的对应参数

### 初始化环境
```
owmc --init
```
### 检查环境
```
owmc --envcheck all
```
### 生成安装包
假设用户的fisco-bcos程序放在/usr/local/bin/fisco-bcos。

**tips**用户可以使用whereis fisco-bcos查找具体位置
```
$ owmc --build ./conf/sample_12345_v1.0.conf /usr/local/bin/fisco-bcos
```
### 部署安装包
```
$ owmc --publish 12345:v1.0.0 12346:v1.0.0
```
### 启动节点
```
$ owmc --start all
```
### 检查节点启动情况
```
$ owmc --check all
```
### 停止节点
```
$ owmc --stop all
```
上述操作完成了两条链的搭建，更多操作请访问[操作手册](https://fisco-bcos-documentation.readthedocs.io/zh_CN/feature-multichain/docs/mulchain/operator.html)
