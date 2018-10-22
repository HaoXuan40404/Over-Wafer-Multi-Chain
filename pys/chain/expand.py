import os
import sys
import shutil

from pys import path
from pys import utils
from pys.log import logger
from pys.log import consoler
from pys.chain import parser
from pys.chain import data
from pys.node import build
from pys.node import temp_node
from pys.exp import MCError
from pys.node.bootstrapsnode import P2pHosts
from pys.node.bootstrapsnode import P2pHost

from pys.node.fisco_version import Fisco

def expand_cc(cc, fisco_path, genesisjson, bootstrapnodesjson):

    chain = cc.get_chain()
    port = cc.get_port()

    if os.path.exists(chain.data_dir()): 
        # expand on exist chain, check common、 genesis.json、 bootstrapnodes.json file exist.
        if not os.path.exists(chain.data_dir() + '/common'):
            raise MCError(' chain dir exist ,but common dir not exist, chain_id %s and chain_version %s' % (chain.get_id(), chain.get_version()))
        if not os.path.exists(chain.data_dir() + '/genesis.json'):
            raise MCError(' chain dir exist ,but genesis.json not exist, chain_id %s and chain_version %s' % (chain.get_id(), chain.get_version()))
        if not os.path.exists(chain.data_dir() + '/bootstrapnodes.json'):
            raise MCError(' chain dir exist ,but bootstrapnodes.json not exist, chain_id %s and chain_version %s' % (chain.get_id(), chain.get_version()))
        
        # expand install dir for every server
        for node in cc.get_nodes():
            try:
                build.expand_host_dir(chain, node, port)
            except Exception as e:
                continue
    else:
        try:
            # check if fisco-bcos、genesis.json、bootstrapsnode.json exist.
            if not os.path.exists(fisco_path):
                raise MCError(
                    ' fisco bcos not exist, fisco bcos path is %s' % fisco_path)
            if not os.path.exists(genesisjson):
                raise MCError(
                    ' genesis.json not exist, genesis.json path is %s' % genesisjson)
            if not os.path.exists(bootstrapnodesjson):
                raise MCError(
                    ' bootstrapnodes.json not exist, bootstrapnodes.json path is %s' % bootstrapnodesjson)
        
             # parser fisco-bcos version and check it.
            fisco = Fisco(fisco_path)
            if not fisco.is_13_version():
                logger.error(' fisco-bcos is not 1.3.x version, not support now, versin is %s', fisco)
                raise MCError(' fisco-bcos is not 1.3.x version, not support now, versin is %s' % fisco)

            os.makedirs(chain.data_dir())
            shutil.copy(genesisjson, chain.data_dir() + '/')
            shutil.copy(bootstrapnodesjson, chain.data_dir() + '/')

            # create common dir
            build.build_common_dir(chain, fisco)
            # build install dir for every server
            for node in cc.get_nodes():
                build.expand_host_dir(chain, node, port)

        except Exception as e:
            if os.path.exists(chain.data_dir()):
                shutil.rmtree(chain.data_dir())
            logger.error(' expand failed, chain id is %s, chain version is %s, exception is %s.',
                         chain.get_id(), chain.get_version(), e)
        else:
            consoler.info('\texpand package for chain %s version %s success.',
                          chain.get_id(), chain.get_version())

    logger.info('expand end, cc is %s', cc)
    

def chain_expand(cfg, args):
    """expand operation 
    
    Arguments:
        cfg {string} -- config file path
        fisco_path {string} -- fisco-bcos file path
        genesisjson {string} -- genesis.json file path
        bootstrapnodesjson {string} -- bootstrapsnodes.json file path
    """

    fisco_path = ''
    genesisjson = ''
    bootstrapnodesjson = ''

    if len(args) > 1:
        fisco_path = args[0]
    if len(args) > 2:
        genesisjson = args[1]
    if len(args) > 3:
        bootstrapnodesjson = args[2]

    try:
        # parser config file    
        cc = parser.do_parser(cfg)
        chain = cc.get_chain()
        consoler.info(' parser config %s success, chain_id is %s, chain_version is %s' % (
            cfg, chain.get_id(), chain.get_version()))
        logger.info('expand operation, parser config success, cc is %s', cc)

    except Exception as e:
        consoler.error(
            ' invalid config format parser failed, config is %s, exception is %s', cfg, e)
    else:
        expand_cc(cc, fisco_path, genesisjson, bootstrapnodesjson)