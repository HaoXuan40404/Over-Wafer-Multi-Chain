# OWMC使用手册

Over-Wafer-Multi-Chain(OWMC)是针对机构内同时部署多条链的物料包。操作者可以在单台运维服务器上通过配置ssh与多台服务器进行交互，从而快速在多台服务器上部署多条区块链，从而对多个区块链网络进行维护，检测，发布，运维的工具。

使用OWMC可以在运维服务器上对后台服务器批量检测生产环境，生成安装包，进行启动，停止，检测，发布，扩容等操作。同时在区块链网络出现问题时，可以对区块链网络进行诊断，检测等操作。

列如：在一台服务器上，配置好与其他服务器的ssh密钥，生成三条链，每条链在三台服务器上有三个节点，将安装包推给对应服务器，启动节点，组成三条区块链网络。

OWMC支持使用ansible维护和自主维护方式，如下图所示：

![](https://github.com/HaoXuan40404/Over-Wafer-Multi-Chain/blob/dev/doc/owmc-1.jpg)

1.使用ansbile

用户在运维服务器上生成安装包，使用ansible对后台服务器进行操作，将安装包推送给后台服务器，启动节点，对区块链网络进行维护。

2.自主维护

用户在运维服务器上生成安装包，采用自己机构运维管理方式，将安装包推送到后台服务器，启动节点，对区块链网络进行维护。


OWMC自动化运维管理工具的示意图如下所示：

![](https://github.com/HaoXuan40404/Over-Wafer-Multi-Chain/blob/dev/doc/owmc-build-1.jpg)

上图以生成安装包，并推送到对应服务器上为例。

用户在运维服务器上使用build命令生成多链安装包，之后使用publish命令，将安装包推送到对应后台服务器上，对多条链进行操作。



## [系统环境检测](https://github.com/HaoXuan40404/Over-Wafer-Multi-Chain/blob/dev/doc/envcheck.md)
FISCO BCOS对网络、yum源等外部环境存在依赖, 为减少搭建过程中遇到的问题,建议在使用之前对整个搭建的环境进行检查。  


**用户可以使用 [OWMC自主维护使用手册]()自行导出安装包，不用ansible进行维护**
部署OWMC时需要用到ansible进行多服务器的数据流传输，ansible是基于Python开发，集合了众多运维工具的优点，实现了批量系统配置、批量程序部署、批量运行命令等功能的一个自动化运维工具。本文是OWMC ansible的配置文档。


## [OWMC极简操作手册](https://github.com/HaoXuan40404/Over-Wafer-Multi-Chain/blob/dev/doc/sample.md)
用户通过本章可以快速体验搭建一条区块链

## [OWMC使用手册](https://github.com/HaoXuan40404/Over-Wafer-Multi-Chain/blob/dev/doc/operator.md)
本章是物理OWMC的具体使用手册，包括相关命令参数设置，输出说明和一些例子。


## [OWMC自主维护使用手册](https://github.com/HaoXuan40404/Over-Wafer-Multi-Chain/blob/dev/doc/export.md)
如果用户不希望使用ansible进行操作，OWCM也支持用户如同物料包操作一般，将安装包导出到自己需要的路径下进行维护。


## [FAQ](https://github.com/HaoXuan40404/Over-Wafer-Multi-Chain/blob/dev/doc/FAQ.md)
