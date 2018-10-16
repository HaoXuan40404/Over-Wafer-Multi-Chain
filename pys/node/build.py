#coding:utf-8

import os
import shutil
import json

from pys import utils
from pys import path
from pys import ca

from pys.node import config
from pys.log import logger

def build_node_dir(dir, node_dir, chain, port, node):
    """build node dir.
    
    Arguments:
        dir {string} -- base dir
        node_dir {string} -- node dir
        chain {Chain} -- chain info
        port {Port} -- port info
        node {Node} -- node info
    
    Raises:
        Exception -- exception description

    one node directory structure is as：
    node/
        ├── config.json
        ├── genesis.json
        ├── data
        ├── log
        ├── log.conf
        ├── start.sh
        └── stop.sh
        ├── check.sh
    """

    logger.info('node_dir => %s, chain => %s, node => %s, port => %s', node_dir, chain, node, port)

    if os.path.isdir(node_dir):
        raise Exception('node dir aleady exist, node_dir ', node_dir)
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
    # shutil.copy(dir + '/bootstrapnodes.json', node_dir + '/data')

    # generate node ca
    ca.generator_node_ca(node_dir + '/data', node.get_p2p_ip(), ca.get_agent_ca_path())

def build_install_dir(dir, chain, port, node, temp=None):
    """build install pacakge of one server.
    
    Arguments:
        dir {string} -- base dir
        chain {Chain} -- chain info, chain id and chain version.
        port {Port} -- port info.
        node {Node} -- node info.
        temp {Temp} -- temp node, if temp is not None, register the node info to the node manager info.
    
    Raises:
        Exception -- exception description
    """

    logger.info('dir => %s, node => %s, port => %s', dir, node, port)

    node_dir = dir + ('/%s' % node.get_host_ip())
    if os.path.isdir(node_dir):
        raise Exception('node dir aleady exist, dir ', node_dir)

    os.makedirs(node_dir)

    for index in range(node.get_node_num()):
        # create dir for every node on the server
        build_node_dir(dir, node_dir + ('/node%d' % index), chain, port.to_port(index), node)
        # register node info to node manager contract
        if  not temp is None:
            temp.registerNode(dir, node_dir + ('/node%d' % index) + '/data/node.json')

    logger.info('build_install_dir end.') 