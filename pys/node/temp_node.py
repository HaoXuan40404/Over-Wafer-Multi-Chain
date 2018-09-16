#coding:utf-8

import os
import shutil
import time

import config
import commands

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
    #拷贝fisco-bcos文件
    shutil.copy(path.get_fisco_dir() + '/fisco-bcos', dir + '/temp/node/')

    shutil.copy(dir + '/temp/node/sdk/ca.crt', dir + '/temp/web3sdk/conf')
    shutil.copy(dir + '/temp/node/sdk/client.keystore', dir + '/temp/web3sdk/conf')
    cfg_json = config.build_config_json('12345', port.get_rpc_port(), port.get_p2p_port(), port.get_channel_port())
    with open(dir + '/temp/node/config.json',"w+") as f:
            f.write(cfg_json)

    old = 'NODE@HOSTIP'
    new = 'node0@127.0.0.1:%d' % port.get_channel_port()
    utils.replace(dir + '/temp/web3sdk/conf/applicationContext.xml', old, new)
    logger.info('build temp node end')

def start_temp_node(dir):
    '''
    '''
    cmd = 'bash %s/temp/node/start.sh' % dir
    status, output = commands.getstatusoutput(cmd);
    logger.debug('start status, status is %d, output is %s', status, output)

    # sleep for temp start
    time.sleep(10)

    cmd = 'bash %s/temp/node/check.sh' % dir
    status, output = commands.getstatusoutput(cmd)
    logger.debug('check status, status is %d, output is %s', status, output)

    if utils.valid_string(output) and (output.find('node is running') != -1):
        return True
    else:
        return False

def stop_temp_node(dir):
    '''
    '''
    cmd = 'bash %s/temp/node/stop.sh' % dir
    status, output = commands.getstatusoutput(cmd)
    logger.debug('stop status, status is %d, output is %s', status, output)

def clean_temp_node(dir):
    '''
    '''
    stop_temp_node(dir)
    os.removedirs(dir + '/temp')

def registerNode(dir, nodejson):
    '''
    '''
    cmd = 'bash %s/temp/web3sdk/bin/web3sdk NodeAction registerNode file:%s' % (dir, nodejson)
    status, output = commands.getstatusoutput(cmd)

    logger.debug('register status, status is %d, output is %s', status, output)