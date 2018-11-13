# OWMC搭建范例
本章我们会给出一个示例，假设用户使用一台运维服务器，拥有三条托管服务器，hostip分别为127.0.0.1,127.0.0.2,127.0.0.3。让用户在运维服务器上快速搭建一条链在127.0.0.1上有三个节点的区块链



## 下载源码
```
git clone https://github.com/HaoXuan40404/Over-Wafer-Multi-Chain.git
git checkout dev
```

## 配置环境依赖

相关操作参考[环境依赖](https://github.com/HaoXuan40404/Over-Wafer-Multi-Chain/blob/dev/doc/envcheck.md)

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
--ansibleinit ./conf/hosts.conf
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
### 确定安装路径
在部署安装包之前，用户可以修改推送的路径，修改./conf/mchain.conf
```
$ vim ./conf/mchain.conf
```
其中dir=/data/app的/data/app即为用户希望推送到对应服务器的位置，请确保所在用户拥有访问该路径的权限。
### 部署安装包

###
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
