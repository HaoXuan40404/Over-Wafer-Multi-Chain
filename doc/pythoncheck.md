# OWMC python2.7配置文档
OWMC需要使用python2.7来生成相关安装包，本文是python2.7的配置文档。有些系统默认的python版本为3.X版本，因此需要对系统的python版本进行配置

## 安装

### python2.7安装
centOS系统

centos系统自带python2.7版本，一般情况下不需要安装，如果python版本比2.7或3.5版本更低，则需要进行更新操作
```
使用
$ python -V
观察python版本是否满足要求(高于2.7或3.5)
```
如果不满足，执行
```
sudo yum install python2.7
如果epel中没有python对应版本，执行
$ sudo yum install epel-release
$ sudo yum install bzip2-devel
```

最后安装包configparser
```
$ sudo npm install python-pip
$ sudo pip install configparser
```
ubuntu系统
```
$ sudo apt-get update
$ sudo apt-get install python2.7
如果epel中没有python对应版本，执行
$ sudo add-apt-repository ppa:fkrull/deadsnakes-python2.7
$ sudo apt-get update
$ sudo apt-get install python2.7
$ sudo rm /usr/local/bin/python
$ sudo ln -s /usr/bin/python2.7 /usr/local/bin/python
$ sudo ln -fs usr/bin/python2.7/bin/pip /usr/bin/pip
```
最后安装包configparser
```
$ sudo apt-get install python-pip
$ sudo pip install configparser
```
如果需要问题，可以使用
```
sudo apt-get install --reinstall python-minimal
sudo apt-get install --reinstall python2.7
```
进行修复


## 检测

```
$ python -V
$ pip -V
```
观察是否提示为
Python 2.7.X 或3.5.X 以上版本
pip X.X.X from /usr/lib/pythonX.X/dist-packages (python X.X) 观察版本是否与python对应
```
$ python
>>> import configparser
>>> exit()
```
观察是否报错
