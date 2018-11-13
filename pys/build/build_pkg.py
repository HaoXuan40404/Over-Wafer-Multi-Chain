#coding:utf-8

import json
import os
import shutil

from pys import path
from pys.tool import ca, utils
from pys.data_mgr.package import HostNodeDirs
from pys.error.exp import MCError
from pys.log import logger
from pys.build.config.config import Config

def build_node_dir(chain, node, fisco, port, index):
    """create node${index} dir.
    
    Arguments:
        chain {Chain} -- chain info
        node {Node} -- node info
        fisco {Fisco} -- fisco info
        port {Port} -- port info
        index {int} -- index info
    
    Raises:
        Exception -- exception description

    one node directory structure is as:
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

    logger.info('chain is %s, node is %s, index is %s',
                chain, node, index)
    node_dir = chain.data_dir() + '/' + node.get_host_ip() + \
        '/node' + str(index) + '/'
    if os.path.exists(node_dir):
        logger.warn(
            ' skip, node%d already exist, chain is %s, node is %s', index, chain, node)
        return

    os.makedirs(node_dir)
    shutil.copy(path.get_path() + '/tpl/log.conf', node_dir)
    shutil.copy(path.get_path() + '/scripts/node/node_start.sh',
                node_dir + '/start.sh')
    shutil.copy(path.get_path() + '/scripts/node/node_stop.sh',
                node_dir + '/stop.sh')
    shutil.copy(path.get_path() + '/scripts/node/node_check.sh',
                node_dir + '/check.sh')
    shutil.copy(path.get_path() + '/scripts/node/node_diagnose.sh',
                node_dir + '/diagnose.sh')

    cfg = Config(chain.get_id(), port.get_rpc_port(), port.get_p2p_port(), port.get_channel_port(), fisco.is_gm())
    cfg.writeFile(node_dir + '/config.json')

    os.makedirs(node_dir + '/data')
    os.makedirs(node_dir + '/log')

    # copy bootstrapnodes.json、genesis.json to correspond dir
    if os.path.exists(chain.data_dir() + '/bootstrapnodes.json'):
        shutil.copy(chain.data_dir() + '/bootstrapnodes.json', node_dir + '/data')
    if os.path.exists(chain.data_dir() + '/genesis.json'):
        shutil.copy(chain.data_dir() + '/genesis.json', node_dir + '/')

    if fisco.is_gm():
        ca.generator_node_ca(ca.get_GM_agent_path(),
            node_dir + '/data', 'node' + str(index), True)
        shutil.copytree(ca.get_GM_agent_path() + '/sdk', node_dir + '/data/sdk')
        shutil.copy(ca.get_GM_agent_path() + '/sdk/ca.crt', node_dir + '/data/')
        shutil.copy(ca.get_GM_agent_path() + '/sdk/ca.key', node_dir + '/data/')
        shutil.copy(ca.get_GM_agent_path() + '/sdk/server.crt', node_dir + '/data/')
        shutil.copy(ca.get_GM_agent_path() + '/sdk/server.key', node_dir + '/data/')
    else:
        ca.generator_node_ca(
            ca.get_agent_ca_path(), node_dir + '/data', 'node' + str(index))


    logger.info(' build_node_dir end. ')

def build_host_dir(chain, node, port, fisco, temp=None):
    """build install pacakge of one server.
    
    Arguments:
        chain {Chain} -- chain info, chain id and chain version.
        node {Node} -- node info.
        port {Port} -- port info.
        fisco {Fisco} -- fisco info.
        temp {Temp} -- temp node, if temp is not None, register the node info to the node manager info.
    
    Raises:
        Exception -- exception description
    """

    logger.info('chain => %s, node => %s, port => %s', chain, node, port)

    host_dir = chain.data_dir() + '/' + node.get_host_ip()
    if os.path.exists(host_dir):
        logger.warn('%s dir already exist, chain is %s',
                    node.get_host_ip(), chain)
        return
    os.makedirs(host_dir)

    for index in range(node.get_node_num()):
        # create dir for every node on the server
        build_node_dir(chain, node, fisco, port.to_port(index), index)
        # register node info to node manager contract
        if not temp is None:
            if fisco.is_gm():
                temp.register(host_dir + ('/node%d' %
                                          index) + '/data/gmnode.json')
            else:
                temp.register(host_dir + ('/node%d' %
                                          index) + '/data/node.json')

    logger.info('build_host_dir end.')

def build_common_dir(chain, fisco):
    """build common directory for version of the chain
    
    Arguments:
        dir {string} -- create the directory for the common directory

    common/
        ├── check.sh
        ├── fisco-bcos
        ├── diagnose.sh
        ├── node_manager.sh
        ├── register.sh
        ├── rmlogs.sh
        ├── scripts
        ├── start.sh
        ├── stop.sh
        ├── unregister.sh
        └── web3sdk
    """
    # dir = chain.data_dir()
    # create common dir
    com_dir = chain.data_dir() + '/common'
    os.makedirs(com_dir)

    # copy fisco-bcos file
    shutil.copy(fisco.get_fisco_path(), com_dir)
    # web3sdk
    shutil.copytree(path.get_path() +
                    '/tpl/web3sdk', com_dir + '/web3sdk')

    if fisco.is_gm():
        # copy ca.crt to web3sdk conf dir
        shutil.copy(ca.get_GM_agent_path() + '/sdk/ca.crt',
                    com_dir + '/web3sdk/conf')
        # copy client.keystore to web3sdk conf dir
        shutil.copy(ca.get_GM_agent_path() + '/sdk/client.keystore',
                    com_dir + '/web3sdk/conf')
        # shutil.move(com_dir + '/web3sdk/conf/applicationContext_GM.xml', 
        #            com_dir + '/web3sdk/conf/applicationContext.xml')

    else:
        # copy ca.crt to web3sdk conf dir
        shutil.copy(ca.get_agent_ca_path() + '/sdk/ca.crt',
                    com_dir + '/web3sdk/conf')
        # copy client.keystore to web3sdk conf dir
        shutil.copy(ca.get_agent_ca_path() + '/sdk/client.keystore',
                    com_dir + '/web3sdk/conf')
        # shutil.move(com_dir + '/web3sdk/conf/applicationContext_NB.xml', 
        #            com_dir + '/web3sdk/conf/applicationContext.xml')

    # copy scripts to common dir
    shutil.copy(path.get_path() + '/scripts/node/start.sh', com_dir)
    shutil.copy(path.get_path() + '/scripts/node/stop.sh', com_dir)
    shutil.copy(path.get_path() + '/scripts/node/check.sh', com_dir)
    shutil.copy(path.get_path() + '/scripts/node/register.sh', com_dir)
    shutil.copy(path.get_path() + '/scripts/node/unregister.sh', com_dir)
    shutil.copy(path.get_path() + '/scripts/node/diagnose.sh', com_dir)
    shutil.copy(path.get_path() + '/scripts/node/monitor.sh', com_dir)
    shutil.copy(path.get_path() + '/scripts/node/rmlogs.sh', com_dir)           

    # copy scripts dir to common dir
    shutil.copytree(path.get_path() + '/scripts', com_dir + '/scripts')

    logger.debug(' build common dir end, chain is %s', chain)

def expand_host_dir(chain, node, port, fisco):
    """expand install pacakge of the server.
    
    Arguments:
        chain {Chain} -- chain info, chain id and chain version.
        node {Node} -- node info.
        port {Port} -- port info.
    
    Raises:
        Exception -- exception description
    """

    logger.info(' chain is %s, node is %s, port is %s',chain, node, port)

    h = HostNodeDirs(chain.get_id(), chain.get_version(), node.get_host_ip())
    index = h.get_max_index()
    append_host_dir = False

    if not h.exist():
        h.create()
        append_host_dir = True
        logger.info(
            ' append host dir, chain is %s, node is %s, index is %s.', chain, node, index)
    else:
        logger.info(
            ' append node dir, chain is %s, node is %s, index is %s.', chain, node, index)

    try:
        # create node dir
        for i in range(node.get_node_num()):
            build_node_dir(chain, node, fisco, port.to_port(i), index + i + 1)
    except Exception as e:
        logger.error(' expand operation failed, chain is %s, node is %s, append_host is %s, e is %s ',
                     chain, node, append_host_dir, e)
        # Delete the created folder
        if append_host_dir:
            h.remove()
        else:
            for i in range(node.get_node_num()):
                # remove node dir
                node_dir = chain.data_dir() + '/' + node.get_host_ip() + '/' + str(index + i)
                if os.path.exists(node_dir):
                    shutil.rmtree(node_dir)
        # raise exception again
        raise e

    logger.info(' expand_host_dir end.')
