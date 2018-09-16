#coding:utf-8

import os
import shutil
import json

from pys import utils
from pys import path
from pys import ca

from pys.node import config
from pys.log import logger

def build_install_dir(dir, chain, port, node):
    '''
    构建一个节点的安装包目录结构
    '''
    logger.info('dir => %s, node => %s, port => %s', dir, node, port)

    node_dir = dir + ('/%s' % node.get_host_ip())
    if os.path.isdir(node_dir):
        raise Exception('node dir aleady exist, dir ', node_dir)

    os.makedirs(node_dir)

    shutil.copy(path.get_path() + '/scripts/start.sh', node_dir)
    shutil.copy(path.get_path() + '/scripts/stop.sh', node_dir)
    shutil.copy(path.get_path() + '/scripts/check.sh', node_dir)
    shutil.copy(path.get_path() + '/scripts/register.sh', node_dir)
    shutil.copy(path.get_path() + '/scripts/unregister.sh', node_dir)
    shutil.copytree(path.get_path() + '/tpl/web3sdk', node_dir + '/web3sdk')

    old = 'NODE@HOSTIP'
    new = 'node0@127.0.0.1:%d' % port.get_channel_port()
    utils.replace(node_dir + '/web3sdk/conf/applicationContext.xml', old, new)

    index = 0
    while index < node.get_node_num():
        subdir = node_dir + ('/node%d' % index)
        os.makedirs(subdir)
        
        shutil.copy(path.get_path() + '/tpl/log.conf', subdir)
        shutil.copy(path.get_path() + '/scripts/node_start.sh', subdir + '/start.sh')
        shutil.copy(path.get_path() + '/scripts/node_stop.sh', subdir + '/stop.sh')
        shutil.copy(path.get_path() + '/scripts/node_check.sh', subdir + '/check.sh')

        cfg_json = config.build_config_json(chain.get_id(), port.get_rpc_port() + index, port.get_p2p_port() + index, port.get_channel_port() + index)
        with open(subdir + '/config.json',"w+") as f:
            f.write(cfg_json)

        os.makedirs(subdir + '/data')
        shutil.copy(dir + '/bootstrapnodes.json', subdir + '/data')

        #节点证书
        

        index += 1

    logger.info('build_install_dir end.')