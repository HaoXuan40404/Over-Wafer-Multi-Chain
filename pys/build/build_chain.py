import os
import sys
import shutil

from pys.tool import utils
from pys.log import logger
from pys.build import build_pkg
from pys.build import temp_node
from pys.data_mgr.port import AllChainPort
from pys.error.exp import MCError
from pys.fisco import god

def build(cc, fisco):
    """build all install package for one chain base on cc 

    Arguments:
        cc {ConfigConf} -- ConfigConf object  
        fisco {Fisco} -- Fisco object

    Raises:
        Exception -- exception description
    """

    logger.info('building, cc is %s, fisco is %s', cc, fisco)

    port = cc.get_port()
    chain = cc.get_chain()
    chain_id = chain.get_id()
    chain_version = chain.get_version()

    # create dir base on version of the chain.
    if os.path.isdir(chain.data_dir()):
        raise MCError('chain_id:%s chain_version:%s aleady exist !!!.' %
                      (chain_id, chain_version))

    try:
        dir = chain.data_dir()

        acp = AllChainPort()
        
        # port check
        for node in cc.get_nodes():
            for index in range(node.get_node_num()):
                # create dir for every node on the server
                acp.port_conflicts_outside_chain(chain.get_id(), node.get_host_ip(), port.to_port(index))

        os.makedirs(dir)

        # generate bootstrapsnode.json
        utils.create_bootstrapnodes(cc.get_nodes(), port, dir)

        # create common dir
  
        build_pkg.build_common_dir(chain, fisco)
        if fisco.is_gm():
            # create temp node for export genesis.json file
            temp_node.GM_temp_node_build(dir, port, fisco)
        else:
            # create temp node for export genesis.json file
            temp_node.temp_node_build(dir, port, fisco)
        # start temp node
        temp_node.start_temp_node(dir, port)

        # build install dir for every server
        for node in cc.get_nodes():
            build_pkg.build_host_dir(chain, node, port, fisco, temp_node)

        # stop temp node and export for genesis.json file
        temp_node.stop_temp_node(dir)
        temp_node.export_genesis(dir)
        temp_node.clean_temp_node(dir)
    

        # copy genesis.json bootstrapnodes.json
        for node in cc.get_nodes():
            for index in range(node.get_node_num()):
                shutil.copy(dir + '/genesis.json', dir + '/' +
                            node.get_host_ip() + '/node' + str(index))

        utils.replace(dir + '/common/web3sdk/conf/applicationContext.xml',
                      'NODE@HOSTIP', 'node0@127.0.0.1:%d' % port.get_channel_port())

        logger.info(' build end ok, chain is %s', chain)

    except Exception as e:
        temp_node.clean_temp_node(dir)
        if os.path.exists(dir):
            shutil.rmtree(dir)

        raise MCError(' build package for chain %s version %s failed, exception is %s' % (
            chain_id, chain_version, e))
