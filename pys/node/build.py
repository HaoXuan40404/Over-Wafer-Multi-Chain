#coding:utf-8

import json
import os
import shutil

from pys import ca, path, utils
from pys.chain.package import HostNodeDirs
from pys.exp import MCError
from pys.log import logger
from pys.node import config
# import sys
# reload(sys)
# sys.setdefaultencoding('utf-8')


def build_node_dir(chain, node, fisco, port, index, cert_path=''):
    """create node${index} dir.
    
    Arguments:
        chain {Chain} -- chain info
        node {Node} -- node info
        fisco {Fisco} -- fisco info
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

    cfg_json = config.build_config_json(chain.get_id(
    ), port.get_rpc_port(), port.get_p2p_port(), port.get_channel_port(), fisco.is_gm())
    with open(node_dir + '/config.json', "w+") as f:
        f.write(cfg_json)

    os.makedirs(node_dir + '/data')
    os.makedirs(node_dir + '/log')

    # copy bootstrapnodes.json、genesis.json to data fir
    if os.path.exists(chain.data_dir() + '/bootstrapnodes.json'):
        shutil.copy(chain.data_dir() + '/bootstrapnodes.json', node_dir + '/data')
    if os.path.exists(chain.data_dir() + '/genesis.json'):
        shutil.copy(chain.data_dir() + '/genesis.json', node_dir + '/data')

    if fisco.is_gm():
        ca.gm_generator_node_ca(
            node_dir + '/data', 'node' + str(index), ca.get_GM_ca_path())
    else:
        # ca.generator_node_ca(node_dir + '/data',
        #                      node.get_p2p_ip(), ca.get_agent_ca_path())
        if cert_path == '':
            ca.new_generator_node_ca(ca.get_agent_ca_path(),
                                node_dir + '/data', 'node' + str(index))
        else:
            try:
                shutil.copy(cert_path + '/' + str(chain.get_id) + '/' + str(chain.get_version) + '/node' + str(index) + '/agency.crt', node_dir + '/data')
                shutil.copy(cert_path + '/' + str(chain.get_id) + '/' + str(chain.get_version) + '/node' + str(index) + '/node.csr', node_dir + '/data')
                shutil.copy(cert_path + '/' + str(chain.get_id) + '/' + str(chain.get_version) + '/node' + str(index) + '/node.json', node_dir + '/data')
                shutil.copy(cert_path + '/' + str(chain.get_id) + '/' + str(chain.get_version) + '/node' + str(index) + '/node.key', node_dir + '/data')
                shutil.copy(cert_path + '/' + str(chain.get_id) + '/' + str(chain.get_version) + '/node' + str(index) + '/node.nodeid', node_dir + '/data')
                shutil.copy(cert_path + '/' + str(chain.get_id) + '/' + str(chain.get_version) + '/node' + str(index) + '/node.private', node_dir + '/data')
                shutil.copy(cert_path + '/' + str(chain.get_id) + '/' + str(chain.get_version) + '/node' + str(index) + '/node.pubkey', node_dir + '/data')
                shutil.copy(cert_path + '/' + str(chain.get_id) + '/' + str(chain.get_version) + '/node' + str(index) + '/node.serial', node_dir + '/data')
                shutil.copy(cert_path + '/' + str(chain.get_id) + '/' + str(chain.get_version) + '/node' + str(index) + '/ca.crt', node_dir + '/data')
                shutil.copy(cert_path + '/' + str(chain.get_id) + '/' + str(chain.get_version) + '/node' + str(index) + '/node.crt', node_dir + '/data')
            except Exception as e:
                logger.error(' Copy cert failed! %s.', e)
                return 1


    logger.info(' build_node_dir end. ')

def build_host_dir(chain, node, port, fisco, temp=None, cert_path = ''):
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
        if cert_path == '':
            build_node_dir(chain, node, fisco, port.to_port(index), index)
        else:
            build_node_dir(chain, node, fisco, port.to_port(index), index, cert_path)
        # register node info to node manager contract
        if not temp is None:
            if fisco.is_gm():
                temp.registerNode(chain.data_dir(), host_dir + ('/node%d' %
                                                   index) + '/data/gmnode.json')
            else:
                temp.registerNode(chain.data_dir(), host_dir + ('/node%d' %
                                                   index) + '/data/node.json')

    logger.info('build_host_dir end.')

def build_common_dir(chain, fisco,cert_path =''):
    """build common directory for version of the chain
    
    Arguments:
        dir {string} -- create the directory for the common directory

    common/
        ├── check.sh
        ├── fisco-bcos
        ├── monitor.sh
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

    if fisco.is_gm():
        # web3sdk
        shutil.copytree(path.get_path() +
                        '/tpl/GM_temp_node/web3sdk', com_dir + '/web3sdk')
        # copy ca.crt to web3sdk conf dir
        shutil.copy(ca.get_ca_path() + '/GM/node0/data/sdk/ca.crt',
                    com_dir + '/web3sdk/conf')
        # copy client.keystore to web3sdk conf dir
        shutil.copy(ca.get_ca_path() + '/GM/node0/data/sdk/client.keystore',
                    com_dir + '/web3sdk/conf')
    else:
        # web3sdk
        if cert_path == '':
            shutil.copytree(path.get_path() + '/tpl/web3sdk', com_dir + '/web3sdk')
            # copy ca.crt to web3sdk conf dir
            shutil.copy(ca.get_agent_ca_path() + '/sdk/ca.crt',
                        com_dir + '/web3sdk/conf')
            # copy client.keystore to web3sdk conf dir
            shutil.copy(ca.get_agent_ca_path() + '/sdk/client.keystore',
                        com_dir + '/web3sdk/conf')
        else:
            shutil.copytree(cert_path + '/sdk',  com_dir + '/web3sdk')
            shutil.copy(cert_path + '/sdk/ca.crt',
                        com_dir + '/web3sdk/conf')
            shutil.copy(cert_path + '/sdk/client.keystore',
                        com_dir + '/web3sdk/conf')


    # copy scripts to common dir
    shutil.copy(path.get_path() + '/scripts/node/start.sh', com_dir)
    shutil.copy(path.get_path() + '/scripts/node/stop.sh', com_dir)
    shutil.copy(path.get_path() + '/scripts/node/check.sh', com_dir)
    shutil.copy(path.get_path() + '/scripts/node/register.sh', com_dir)
    shutil.copy(path.get_path() + '/scripts/node/unregister.sh', com_dir)
    shutil.copy(path.get_path() + '/scripts/node/monitor.sh', com_dir)
    shutil.copy(path.get_path() + '/scripts/node/rmlogs.sh', com_dir)
    shutil.copy(path.get_path() + '/scripts/node/node_manager.sh', com_dir)

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
            build_node_dir(chain, node, fisco, port.to_port(i), index + i)
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
