import os
import sys
import shutil

from pys.tool import utils
from pys.log import logger
from pys.build import build_pkg
# from pys.build import temp_node
from pys.build.temp import Temp
from pys.build.tool import web3_conf_by_chain
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
        temp = None
        acp = AllChainPort()
        # port check
        for node in cc.get_nodes():
            for index in range(node.get_node_num()):
                # create dir for every node on the server
                acp.port_conflicts_outside_chain(chain.get_id(), node.get_host_ip(), port.to_port(index))
        
        dir = chain.data_dir()
        os.makedirs(dir)

        # generate bootstrapsnode.json
        cc.to_p2p_nodes().writeFile(dir + '/bootstrapnodes.json')

        # create common dir
        build_pkg.build_common_dir(chain, fisco)
        # build and start temp node for node info register
        temp = Temp(chain, fisco, port)

        # build install dir for every server
        for node in cc.get_nodes():
            build_pkg.build_host_dir(chain, node, port, fisco, temp)

        # export for genesis.json file
        temp.export()
        temp.clean()

        # copy genesis.json bootstrapnodes.json
        for node in cc.get_nodes():
            for index in range(node.get_node_num()):
                shutil.copy(dir + '/genesis.json', dir + '/' +
                            node.get_host_ip() + '/node' + str(index))
        
        # web3sdk conf
        web3_conf_by_chain(chain, fisco.is_gm())

        logger.info(' build end ok, chain is %s', chain)

    except Exception as e:
        if not temp is None:
            temp.clean()
            
        if os.path.exists(dir):
            shutil.rmtree(dir)

        raise MCError(' build package for chain %s version %s failed, exception is %s' % (
            chain_id, chain_version, e))
