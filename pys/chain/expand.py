#coding:utf-8
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
from pys.chain.parser import ConfigConf

from pys.node.fisco_version import Fisco


def expand_cc(cc, fisco_path, genesisjson, bootstrapnodesjson):

    chain = cc.get_chain()
    port = cc.get_port()

    if os.path.exists(chain.data_dir()): 
        # expand on exist chain, check common、 genesis.json、 bootstrapnodes.json file exist.
        if not os.path.exists(chain.data_dir() + '/common'):
            raise MCError(' chain dir exist ,but common dir not exist, chain_id %s、chain_version %s' % (chain.get_id(), chain.get_version()))
        if not os.path.exists(chain.data_dir() + '/genesis.json'):
            raise MCError(' chain dir exist ,but genesis.json not exist, chain_id %s、chain_version %s' % (chain.get_id(), chain.get_version()))
        if not os.path.exists(chain.data_dir() + '/bootstrapnodes.json'):
            raise MCError(' chain dir exist ,but bootstrapnodes.json not exist, chain_id %s、and chain_version %s' % (chain.get_id(), chain.get_version()))
        
        fisco = Fisco(chain.data_dir() + '/' + 'common' + '/' + 'fisco-bcos')
        # expand install dir for every server
        for node in cc.get_nodes():
            try:
                build.expand_host_dir(chain, node, port, fisco)
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
                build.expand_host_dir(chain, node, port,fisco)

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
        try:
            # parser and check config if valid
            cc = ConfigConf(cfg)
        except Exception as e:
            raise MCError(' expand operation failed, invalid config, exception is %s' % e) 

        expand_cc(cc, fisco_path, genesisjson, bootstrapnodesjson)

    except MCError as me:
        consoler.error(me)
    except Exception as e:
        consoler.error(' Unkown exception, e is %s' % e)