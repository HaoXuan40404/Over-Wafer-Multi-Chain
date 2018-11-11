#coding:utf-8

import os
import shutil
import time

from pys.tool import utils
from pys import path
from pys.log import logger
from pys.log import consoler
from pys.build.config.config import Config
from pys.error.exp import MCError

def GM_temp_node_build(dir, port, fisco):
    """Generate GM temp node package
    
    Arguments:
        dir {string} -- temp node dictionary 
        port {Port} -- port message 
    """

    logger.info('GM build temp node, dir => ' + dir)

    os.makedirs(dir + '/temp')
    shutil.copytree(path.get_path() + '/tpl/web3sdk', dir + '/temp/web3sdk')
    shutil.move(dir + '/temp/web3sdk/conf/applicationContext_GM.xml',
                    dir + '/temp/web3sdk/conf/applicationContext.xml')

    shutil.copytree(path.get_path() + '/tpl/GM_temp_node', dir + '/temp/node')
    #copy GM fisco-bcos
    shutil.copy(fisco.get_fisco_path(), dir + '/temp/node/')

    shutil.copy(dir + '/temp/node/data/sdk/ca.crt', dir + '/temp/web3sdk/conf')
    shutil.copy(dir + '/temp/node/data/sdk/client.keystore', dir + '/temp/web3sdk/conf')

    cfg = Config('12345', port.get_rpc_port(), port.get_p2p_port(), port.get_channel_port(), True)
    cfg.writeFile(dir + '/temp/node/config.json')

    utils.replace(dir + '/temp/web3sdk/conf/applicationContext.xml', 'WEB3SDK_NODES_LIST', '<value>node0@127.0.0.1:%d</value>' % port.get_channel_port())

    logger.info('GM build temp node end')

def temp_node_build(dir, port, fisco):
    """create dir for temp node run
    
    Arguments:
        dir {string} -- the dir where temp node create
        port {Port} -- the port temp node use
    """

    logger.info('build temp node, dir => ' + dir)

    os.makedirs(dir + '/temp')
    shutil.copytree(path.get_path() + '/tpl/web3sdk', dir + '/temp/web3sdk')
    shutil.move(dir + '/temp/web3sdk/conf/applicationContext_NB.xml',
                    dir + '/temp/web3sdk/conf/applicationContext.xml')

    shutil.copytree(path.get_path() + '/tpl/temp_node', dir + '/temp/node')
    #copy fisco-bcos file
    shutil.copy(fisco.get_fisco_path(), dir + '/temp/node/')

    shutil.copy(dir + '/temp/node/sdk/ca.crt', dir + '/temp/web3sdk/conf')
    shutil.copy(dir + '/temp/node/sdk/client.keystore', dir + '/temp/web3sdk/conf')
    cfg = Config('12345', port.get_rpc_port(), port.get_p2p_port(), port.get_channel_port())
    cfg.writeFile(dir + '/temp/node/config.json')

    utils.replace(dir + '/temp/web3sdk/conf/applicationContext.xml', 'WEB3SDK_NODES_LIST', '<value>node0@127.0.0.1:%d</value>' % port.get_channel_port())
    logger.info('build temp node end')

def start_temp_node(dir, port):
    """start temp node
    
    Arguments:
        dir {string} -- temp node dir
        port {Port} -- the port temp node use
    
    Returns:
        bool -- if temp node start success, return True, if not False will return.
    """

    # check port conflicts
    if utils.port_in_use(port.get_rpc_port()):
        logger.warn(' rpc port in use, port is %s', port.get_rpc_port())
        raise MCError(' rpc port(%s) is in use.' % port.get_rpc_port())
  
    if utils.port_in_use(port.get_p2p_port()):
        logger.warn('p2p port in use, port is %s', port.get_p2p_port())
        raise MCError(' p2p port(%s) is in use.' % port.get_p2p_port())

    if utils.port_in_use(port.get_channel_port()):
        logger.warn('channel port in use, port is %s', port.get_channel_port())
        raise MCError(' channel port(%s) is in use.' % port.get_channel_port())

    cmd = 'bash %s/temp/node/start.sh' % dir
    status, output = utils.getstatusoutput(cmd)
    logger.debug(' start status, status is %d, output is %s', status, output)

    # sleep for temp start
    time.sleep(10)

    cmd = 'bash %s/temp/node/check.sh' % dir
    status, output = utils.getstatusoutput(cmd)
    logger.info('check status, status is %d, output is %s', status, output)

    if utils.valid_string(output) and (output.find('is running') != -1):
        # add consoler.log for the reason temp node start failed.
        pass
    else:
        raise MCError(' temp node start failed, outpus is %s' % output)

def stop_temp_node(dir):
    """stop temp node
    
    Arguments:
        dir {string} -- temp node dir
    """

    cmd = 'bash %s/temp/node/stop.sh' % dir
    status, output = utils.getstatusoutput(cmd)
    logger.debug('stop status, status is %d, output is %s', status, output)

def export_genesis(dir):
    """ export genesis.json from temp node
    
    Arguments:
        dir {string} -- temp node dir
        
    Returns:
        bool --  if export success, return True, if not False will return.
    """

    cmd = 'bash %s/temp/node/export.sh %s/%s' % (dir, dir, 'genesis.json')
    status, output = utils.getstatusoutput(cmd)
    if not os.path.exists(dir + '/genesis.json'):
        logger.warn('export genesis.json failed, output is %s', output)
        raise MCError(' export genesis.json failed, dir is %s, output is %s.' % (dir, output))
    else:
        logger.debug('export status, status is %d, output is %s', status, output)

def clean_temp_node(dir):
    """ stop temp node and remove temp node dir
    
    Arguments:
        dir {string} -- temp node dir
    """

    stop_temp_node(dir)
    if os.path.isdir(dir + '/temp'):
        shutil.rmtree(dir + '/temp') 


def registerNode(dir, nodejson):
    """register node info to node manager contract
    
    Arguments:
        dir {string} -- temp node dir 
        nodejson {json string} -- node info
    """

    cmd = 'bash %s/temp/web3sdk/bin/web3sdk NodeAction registerNode file:%s' % (dir, nodejson)
    status, output = utils.getstatusoutput(cmd)

    if status != 0:
        logger.warn('register status, dir is %s, nodejson is %s,status is %d, output is %s', dir, nodejson, status, output)
    else:
        logger.debug('register status, dir is %s, nodejson is %s,status is %d, output is %s', dir, nodejson, status, output)
