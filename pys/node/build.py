#coding:utf-8

import os
import shutil
import json

from pys import utils
from pys import path
from pys import ca

from pys.node import config
from pys.log import logger

def build_install_dir(dir, chain, port, node, temp):
    """构建一台服务器上的安装包, 创建目录结构, 拷贝需要的脚本, 生成节点的证书, 注册节点.
    
    Arguments:
        dir {string} -- 路径
        chain {Chain} -- 节点所属链的版本号与链id
        port {Port} -- 节点需要的端口
        node {Node} -- 节点信息
        temp {Temp} -- 临时节点, 用来注册节点
    
    Raises:
        Exception -- 异常描述
    """

    logger.info('dir => %s, node => %s, port => %s', dir, node, port)

    node_dir = dir + ('/%s' % node.get_host_ip())
    if os.path.isdir(node_dir):
        raise Exception('node dir aleady exist, dir ', node_dir)

    os.makedirs(node_dir)

    # 脚本
    shutil.copy(path.get_path() + '/scripts/node/start.sh', node_dir)
    shutil.copy(path.get_path() + '/scripts/node/stop.sh', node_dir)
    shutil.copy(path.get_path() + '/scripts/node/check.sh', node_dir)
    shutil.copy(path.get_path() + '/scripts/node/register.sh', node_dir)
    shutil.copy(path.get_path() + '/scripts/node/unregister.sh', node_dir)
    shutil.copy(path.get_path() + '/scripts/node/monitor.sh', node_dir)
    shutil.copy(path.get_path() + '/scripts/node/rmlogs.sh', node_dir)
    shutil.copy(path.get_path() + '/scripts/node/node_manager.sh', node_dir)

    """
    fisco-bcos文件, web3sdk提取到上级目录
    """
    #拷贝fisco-bcos文件
    # shutil.copy(path.get_fisco_path(), node_dir)

    # web3sdk
    # shutil.copytree(path.get_path() + '/tpl/web3sdk', node_dir + '/web3sdk')
    # shutil.copy(ca.get_agent_ca_path() + '/sdk/ca.crt', node_dir + '/web3sdk/conf')
    # shutil.copy(ca.get_agent_ca_path() + '/sdk/client.keystore', node_dir + '/web3sdk/conf')
    # utils.replace(node_dir + '/web3sdk/conf/applicationContext.xml', 'NODE@HOSTIP', 'node0@127.0.0.1:%d' % port.get_channel_port())

    for index in range(len(node.get_node_num())):
        subdir = node_dir + ('/node%d' % index)
        os.makedirs(subdir)
        
        shutil.copy(path.get_path() + '/tpl/log.conf', subdir)
        shutil.copy(path.get_path() + '/scripts/node/node_start.sh', subdir + '/start.sh')
        shutil.copy(path.get_path() + '/scripts/node/node_stop.sh', subdir + '/stop.sh')
        shutil.copy(path.get_path() + '/scripts/node/node_check.sh', subdir + '/check.sh')

        cfg_json = config.build_config_json(chain.get_id(), port.get_rpc_port() + index, port.get_p2p_port() + index, port.get_channel_port() + index)
        with open(subdir + '/config.json',"w+") as f:
            f.write(cfg_json)

        os.makedirs(subdir + '/data')
        os.makedirs(subdir + '/log')
        shutil.copy(dir + '/bootstrapnodes.json', subdir + '/data')

        # 生成节点证书
        ca.generator_node_ca(subdir + '/data', node.get_p2p_ip() + '_' + str(index), ca.get_agent_ca_path())
        
        #注册节点到系统合约
        if  not temp is None:
            temp.registerNode(dir, subdir + '/data/node.json')

    logger.info('build_install_dir end.')