# OWMC python2.7配置文档
OWMC需要使用python2.7来生成相关安装包，本文是python2.7的配置文档。有些系统默认的python版本为3.X版本，因此需要对系统的python版本进行配置

## 安装

### python2.7安装
centOS系统

centos系统自带python2版本，一般情况下不需要安装，如果python版本不为2.7，则需要进行如下操作
```
$ sudo yum install zlib-devel
$ sudo yum install bzip2-devel
$ sudo yum install openssl-devel
$ sudo yum install ncurses-devel
$ sudo yum install sqlite-devel
$ wget https://www.python.org/ftp/python/2.7.12/Python-2.7.12.tgz
$ tar xf Python-2.7.12.tgz
$ cd Python-2.7.12
$ ./configure --prefix=/usr/local/python27
$ make
$ make install
$ sudo rm /usr/local/bin/python
$ sudo ln -s /usr/bin/python2.7 /usr/local/bin/python
$ sudo npm install python-pip
$ sudo pip install configparser
```
ubuntu系统
```
$ sudo add-apt-repository ppa:fkrull/deadsnakes-python2.7
$ sudo apt-get update
$ sudo apt-get install python2.7
$ sudo rm /usr/local/bin/python
$ sudo ln -s /usr/bin/python2.7 /usr/local/bin/python
$ sudo ln -fs usr/bin/python2.7/bin/pip /usr/bin/pip
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
Python 2.7.X
pip X.X.X from /usr/lib/python2.7/dist-packages (python 2.7) 观察版本是否与python对应
```
$ python
>>> import configparser
>>> exit()
```
观察是否报错
