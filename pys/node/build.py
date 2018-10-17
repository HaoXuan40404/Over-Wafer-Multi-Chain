#coding:utf-8

import os
import shutil
import json

from pys import utils
from pys import path
from pys import ca

from pys.node import config
from pys.log import logger
from pys.exp import MCError

def build_node_dir(chain, node, port, index):
    """create node${index} dir.
    
    Arguments:
        chain {Chain} -- chain info
        node {Node} -- node info
        port {Port} -- port info
        index {int} -- index info
    
    Raises:
        Exception -- exception description

    one node directory structure is as：
    node${index}/
        ├── config.json
        ├── genesis.json
        ├── data
        ├── log
        ├── log.conf
        ├── start.sh
        └── stop.sh
        ├── check.sh
    """

    logger.info('chain is %s, node is %s, index is %s', chain, node, index)
    node_dir = chain.data_dir() + '/' + node.get_host_ip() + '/node' + str(index) + '/'
    if os.path.exists(node_dir):
        logger.warn(
            ' skip, node%d already exist, chain is %s, node is %s ', index, chain, node)
        return

    os.makedirs(node_dir)
    shutil.copy(path.get_path() + '/tpl/log.conf', node_dir)
    shutil.copy(path.get_path() + '/scripts/node/node_start.sh', node_dir + '/start.sh')
    shutil.copy(path.get_path() + '/scripts/node/node_stop.sh', node_dir + '/stop.sh')
    shutil.copy(path.get_path() + '/scripts/node/node_check.sh', node_dir + '/check.sh')

    cfg_json = config.build_config_json(chain.get_id(), port.get_rpc_port(), port.get_p2p_port(), port.get_channel_port())
    with open(node_dir + '/config.json',"w+") as f:
        f.write(cfg_json)

    os.makedirs(node_dir + '/data')
    os.makedirs(node_dir + '/log')

    # copy bootstrapnodes.json、genesis.json to data fir
    shutil.copy(chain.data_dir() + '/bootstrapnodes.json', node_dir + '/data')
    if os.path.exists(chain.data_dir() + '/genesis.json'):
        shutil.copy(chain.data_dir() + '/genesis.json', node_dir + '/data')

    ca.generator_node_ca(node_dir + '/data', node.get_p2p_ip(), ca.get_agent_ca_path())
    logger.info(' build_node_dir end.')

def build_install_dir(chain, node, port, temp=None):
    """build install pacakge of one server.
    
    Arguments:
        chain {Chain} -- chain info, chain id and chain version.
        node {Node} -- node info.
        port {Port} -- port info.
        temp {Temp} -- temp node, if temp is not None, register the node info to the node manager info.
    
    Raises:
        Exception -- exception description
    """

    logger.info('chain => %s, node => %s, port => %s', chain, node, port)
    dir = chain.data_dir()
    host_dir = dir + '/' + node.get_host_ip()

    if os.path.exists(host_dir):
        logger.warn('%s dir already exist, chain is %s, host is %s', node.get_host_ip(), chain, host)
        return
    os.makedirs(host_dir)

    for index in range(node.get_node_num()):
        # create dir for every node on the server
        build_node_dir(chain, node, port.to_port(index), index)
        # register node info to node manager contract
        if  not temp is None:
            temp.registerNode(dir, host_dir + ('/node%d' % index) + '/data/node.json')

    logger.info('build_install_dir end.') 

def expand_install_dir(chain, node, port):
    """expand install pacakge of one server.
    
    Arguments:
        chain {Chain} -- chain info, chain id and chain version.
        node {Node} -- node info.
        port {Port} -- port info.
    
    Raises:
        Exception -- exception description
    """

    logger.info('chain => %s, node => %s, port => %s', chain, node, port)
    dir = chain.data_dir()
    node_dir = dir + ('/%s' % node.get_host_ip())

    if os.path.exists(node_dir):
        index = 0
        while True:
            if os.path.exists(node_dir + '/node' + index):
                index = index + 1
            else:
                break
        for i in range(node.get_node_num()):
            build_node_dir(chain, node, port.to_port(index), index + i)
            
    else:
        build_install_dir(chain, node, port)

    logger.info('build_install_dir end.') 
