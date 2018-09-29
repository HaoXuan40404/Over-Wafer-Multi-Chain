# FISCO BCOS 物理多链物料包使用手册

FISCO BCOS 物理多链是针对机构内同时部署多条链的物料包。操作者可以在单台运维服务器上通过配置ansible与多台服务器进行交互，从而快速在多台服务器上部署多条区块链。

列如：在一台服务器上，配置好与其他服务器的ssh密钥，生成三条链，每条链在三台服务器上有三个节点，将安装包推给对应服务器，启动节点，组成三条区块链网络。

详见 https://fisco-bcos-documentation.readthedocs.io/zh_CN/feature-multichain/docs/mulchain/index.html