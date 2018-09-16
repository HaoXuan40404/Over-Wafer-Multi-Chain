#coding:utf-8

import os
import shutil

import config

from pys import utils
from pys import path
from pys.log import logger
from pys.node import config

def temp_node_build(dir, port):
    '''
    构建临时节点的运行环境
    '''
    logger.info('build temp node, dir => ' + dir)
    os.makedirs(dir + '/temp')
    shutil.copytree(path.get_path() + '/tpl/web3sdk', dir + '/temp/web3sdk')
    shutil.copytree(path.get_path() + '/tpl/temp_node', dir + '/temp/node')
    cfg_json = config.build_config_json('12345', port.get_rpc_port(), port.get_p2p_port(), port.get_channel_port())
    with open(dir + '/temp/node/config.json',"w+") as f:
            f.write(cfg_json)
            
    old = 'NODE@HOSTIP'
    new = 'node0@127.0.0.1:%d' % port.get_p2p_port()
    utils.replace(dir + '/temp/web3sdk/conf/applicationContext.xml', old, new)
    logger.info('build temp node end')

def start_temp_node(dir):
    '''
    '''
    pass

def stop_temp_node(dir):
    '''
    '''
    pass