# OWMC使用手册

Over-Wafer-Multi-Chain(OWMC)是针对机构内同时部署多条链的物料包。操作者可以在单台运维服务器上通过配置ssh与多台服务器进行交互，从而快速在多台服务器上部署多条区块链，从而对多个区块链网络进行维护，检测，发布，运维的工具。

使用OWMC可以在运维服务器上对后台服务器批量检测生产环境，生成安装包，进行启动，停止，检测，发布，扩容等操作。同时在区块链网络出现问题时，可以对区块链网络进行诊断，检测等操作。

列如：在一台服务器上，配置好与其他服务器的ssh密钥，生成三条链，每条链在三台服务器上有三个节点，将安装包推给对应服务器，启动节点，组成三条区块链网络。

## [系统环境检测](https://github.com/HaoXuan40404/Over-Wafer-Multi-Chain/blob/dev/doc/envcheck.md)
FISCO BCOS对网络、yum源等外部环境存在依赖, 为减少搭建过程中遇到的问题,建议在使用之前对整个搭建的环境进行检查。  

## [软件依赖]()
OWMC在使用时，依赖相关软件的配置，以下是需要的相关软件配置流程


### [java1.8](https://github.com/HaoXuan40404/Over-Wafer-Multi-Chain/blob/dev/doc/javacheck.md)
FISCO BCOS中需要使用Oracle JDK 1.8(java 1.8)或openJDK1.9以上版本, 在CentOS/Ubuntu中默认安装或者通过yum/apt安装的JDK均为openJDK1.8, 并不符合使用的要求, 本文是一份简单的Oracle Java 1.8的配置文档。

### [python安装](https://github.com/HaoXuan40404/Over-Wafer-Multi-Chain/blob/dev/doc/pythoncheck.md)
OWMC需要使用python2.7或3.5以上版本来生成相关安装包，本文是python的配置文档。


### [ansible](https://github.com/HaoXuan40404/Over-Wafer-Multi-Chain/blob/dev/doc/ansiblecheck.md)
**只需要在运维服务器上部署ansible即可**

**用户可以使用 [OWMC自主维护使用手册]()自行导出安装包，不用ansible进行维护**
部署OWMC时需要用到ansible进行多服务器的数据流传输，ansible是基于Python开发，集合了众多运维工具的优点，实现了批量系统配置、批量程序部署、批量运行命令等功能的一个自动化运维工具。本文是OWMC ansible的配置文档。


## [OWMC极简操作手册](https://github.com/HaoXuan40404/Over-Wafer-Multi-Chain/blob/dev/doc/sample.md)
用户通过本章可以快速体验搭建一条区块链

## [OWMC使用手册](https://github.com/HaoXuan40404/Over-Wafer-Multi-Chain/blob/dev/doc/operator.md)
本章是物理OWMC的具体使用手册，包括相关命令参数设置，输出说明和一些例子。


## [OWMC自主维护使用手册](https://github.com/HaoXuan40404/Over-Wafer-Multi-Chain/blob/dev/doc/export.md)
如果用户不希望使用ansible进行操作，OWCM也支持用户如同物料包操作一般，将安装包导出到自己需要的路径下进行维护。




## [FAQ](https://github.com/HaoXuan40404/Over-Wafer-Multi-Chain/blob/dev/doc/FAQ.md)
