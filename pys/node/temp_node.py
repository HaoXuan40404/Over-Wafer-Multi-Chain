#coding:utf-8

import os
import shutil
import time

import config
import commands

from pys import utils
from pys import path
from pys.log import logger
from pys.log import consoler
from pys.node import config

def temp_node_build(dir, port):
    """构建临时节点的运行环境
    
    Arguments:
        dir {string} -- temp节点所在的目录
        port {Port} -- 端口信息
    """

    logger.info('build temp node, dir => ' + dir)

    os.makedirs(dir + '/temp')
    shutil.copytree(path.get_path() + '/tpl/web3sdk', dir + '/temp/web3sdk')

    shutil.copytree(path.get_path() + '/tpl/temp_node', dir + '/temp/node')
    #拷贝fisco-bcos文件
    shutil.copy(path.get_fisco_path(), dir + '/temp/node/')

    shutil.copy(dir + '/temp/node/sdk/ca.crt', dir + '/temp/web3sdk/conf')
    shutil.copy(dir + '/temp/node/sdk/client.keystore', dir + '/temp/web3sdk/conf')
    cfg_json = config.build_config_json('12345', port.get_rpc_port(), port.get_p2p_port(), port.get_channel_port())
    with open(dir + '/temp/node/config.json',"w+") as f:
            f.write(cfg_json)

    old = 'NODE@HOSTIP'
    new = 'node0@127.0.0.1:%d' % port.get_channel_port()
    utils.replace(dir + '/temp/web3sdk/conf/applicationContext.xml', old, new)
    logger.info('build temp node end')

def start_temp_node(dir, port):
    """启动临时节点
    
    Arguments:
        dir {string} -- temp节点所在目录
        port {Port} -- temp节点使用的端口信息
    
    Returns:
        bool -- 启动成功返回True,否则返回False
    """

    # 端口检测
    if utils.port_in_use(port.get_rpc_port()):
        logger.warn(' rpc port in use, port is %s', port.get_rpc_port())
        consoler.error(' temp node rpc port is in use, port is %s', port.get_rpc_port())
        return False
  
    if utils.port_in_use(port.get_p2p_port()):
        logger.warn('p2p port in use, port is %s', port.get_p2p_port())
        consoler.error(' temp node p2p port is in use, port is %s', port.get_p2p_port())
        return False

    if utils.port_in_use(port.get_channel_port()):
        logger.warn('channel port in use, port is %s', port.get_channel_port())
        consoler.error(' temp node channel port is in use, port is %s', port.get_channel_port())
        return False

    cmd = 'bash %s/temp/node/start.sh' % dir
    status, output = commands.getstatusoutput(cmd)
    logger.debug('start status, status is %d, output is %s', status, output)

    # sleep for temp start
    time.sleep(10)

    cmd = 'bash %s/temp/node/check.sh' % dir
    status, output = commands.getstatusoutput(cmd)
    logger.info('check status, status is %d, output is %s', status, output)

    if utils.valid_string(output) and (output.find('is running') != -1):
        return True
    else:
        return False

def stop_temp_node(dir):
    """停止temp节点
    
    Arguments:
        dir {string} -- temp节点所在目录
    """

    cmd = 'bash %s/temp/node/stop.sh' % dir
    status, output = commands.getstatusoutput(cmd)
    logger.debug('stop status, status is %d, output is %s', status, output)

def export_genesis(dir):
    """从temp节点导出genesis.json文件
    
    Arguments:
        dir {string} -- temp节点所在目录
        
    Returns:
        bool -- 启动成功返回True,否则返回False
    """

    cmd = 'bash %s/temp/node/export.sh %s/%s' % (dir, dir, 'genesis.json')
    status, output = commands.getstatusoutput(cmd)
    if not os.path.exists(dir + '/genesis.json'):
        logger.warn('export genesis.json failed, output is %s', output)
        return False
    else:
        logger.debug('export status, status is %d, output is %s', status, output)
        return True

def clean_temp_node(dir):
    """停止temp节点,并且删除temp节点的目录
    
    Arguments:
        dir {string} -- temp节点所在的目录
    """

    stop_temp_node(dir)
    shutil.rmtree(dir + '/temp') 


def registerNode(dir, nodejson):
    """注册一个节点信息,通过启动的temp节点
    
    Arguments:
        dir {string} -- temp节点所在的目录  
        nodejson {json string} -- 节点注册信息
    """

    cmd = 'bash %s/temp/web3sdk/bin/web3sdk NodeAction registerNode file:%s' % (dir, nodejson)
    status, output = commands.getstatusoutput(cmd)

    logger.debug('register status, status is %d', status)