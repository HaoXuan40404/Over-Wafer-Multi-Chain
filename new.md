* ywy 数据记录 哪条链被部署在哪台服务器，记录部署里那些节点 多条链配置该怎么弄 下午过一下 
asher 基本的物料包 操作系统版本检查 java版本检查 移植过来，远程调用，放在scripts/tools下 远程调用shell脚本，主文件夹里pys/tools 远程调用
单节点操作 start_one_node(chainID,hostip)=>多个ip start check版本号之后干掉
monitor 调用web3sdk chain_server

web3sdk->node0 node1 channelport 所有节点的都配置进去，查一个都返回 

命令行优化 build参数用命令行去配置conf参数 多链好不好做--多个文件

多链配置

CA管理模块。
ca.crt agency.cry用户可以放进去
根证书和机构证书只能导入

publish

dest = ansible.get_dir() + '/' + chain_id/


提高简单命令让ansible执行echo，start stop check子命令

整条链干掉 回退操作 停掉删掉 从新发布

只做检查，如果没有权限就FAQ提示出来

命令行提示优化 

对链的诊断 monitor和check 先check再monitor 如果没起来 把log返回
FAQ完善