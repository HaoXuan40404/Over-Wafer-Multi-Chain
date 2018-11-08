################################################################################
Over-Wafer-Multi-Chain(OWMC)搭建工具
################################################################################


.. 什么是OWMC搭建工具

Over-Wafer-Multi-Chain OWMC搭建是针对机构内同时部署多条链的物料包。操作者可以在单台运维服务器上通过配置ansible与多台服务器进行交互，从而快速在多台服务器上部署多条区块链。

列如：在一台服务器上，配置好与其他服务器的ssh密钥，生成三条链，每条链在三台服务器上有三个节点，将安装包推给对应服务器，启动节点，组成三条区块链网络。

用户可以不使用ansible，自主维护生成的安装包，请参考[export.md]()

版本支持

当前OWMC版本号为v1.0.0

执行

```
$ git clone https://github.com/HaoXuan40404/Over-Wafer-Multi-Chain.git

$ git checkout dev
```

OWMC的相关流程如下:


.. toctree::
   :maxdepth: 1

   envcheck.md
   javacheck.md
   pythoncheck.md
   ansiblecheck.md
   sample.md
   operator.md
   export.md
   FAQ.md

