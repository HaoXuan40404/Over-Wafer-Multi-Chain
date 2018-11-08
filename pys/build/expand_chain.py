#coding:utf-8
import os
import sys
import shutil

from pys import path
from pys.tool import utils
from pys.log import logger
from pys.log import consoler
from pys.conf import build_chain_conf
from pys.data_mgr import data
from pys.build import build_chain
from pys.error.exp import MCError
from pys.data_mgr.names import Names
from pys.build.bootstrapsnode import P2pHosts
from pys.build.bootstrapsnode import P2pHost
from pys.conf.build_chain_conf import ConfigConf
from pys.data_mgr.port import AllChainPort

from pys.fisco.version import Fisco

def expand_on_exist_chain(cc):

    chain = cc.get_chain()
    port = cc.get_port()
    chain_id = chain.get_id()
    chain_version = chain.get_version()

    # expand on exist chain, check common、 genesis.json、 bootstrapnodes.json file exist.
    if not os.path.exists(chain.data_dir() + '/common'):
        raise MCError(' chain dir exist ,but common dir not exist, chain_id %s、chain_version %s' % (
            chain_id, chain_version))
    if not os.path.exists(chain.data_dir() + '/genesis.json'):
        raise MCError(' chain dir exist ,but genesis.json not exist, chain_id %s、chain_version %s' % (
            chain_id, chain_version))
    if not os.path.exists(chain.data_dir() + '/bootstrapnodes.json'):
        raise MCError(' chain dir exist ,but bootstrapnodes.json not exist, chain_id %s、and chain_version %s' % (
            chain_id, chain_version))
    
    acp = AllChainPort()
    # port check
    for node in cc.get_nodes():
        for index in range(node.get_node_num()):
            # create dir for every node on the server
            acp.port_conflicts_outside_chain(chain.get_id(), node.get_host_ip(), port.to_port(index))
            acp.port_conflicts_inside_chain(node.get_host_ip(), port.to_port(index) ,chain.get_id(), chain.get_version())

    fisco = Fisco(chain.data_dir() + '/' + 'common' + '/' + 'fisco-bcos')
    
    # expand install dir for every server
    for node in cc.get_nodes():
        try:
            build_chain.expand_host_dir(chain, node, port, fisco)
        except Exception as e:
            logger.error(' expand failed, chain id is %s, chain version is %s, exception is %s.',
                     chain_id, chain_version, e)
            raise MCError(' expand failed, chain id is %s, chain version is %s, exception is %s' % (
            chain_id, chain_version, e))

def expand_on_nonexist_chain(cc, dir):
    
    fisco_path = dir + '/' + 'fisco-bcos'
    genesisjson = dir + '/' + 'genesis.json'
    bootstrapnodesjson = dir + '/' + 'bootstrapnodes.json'
    # check if fisco-bcos、genesis.json、bootstrapsnode.json exist.
    if not os.path.exists(fisco_path):
        raise MCError(
            ' fisco bcos not exist, dir path is %s' % dir)
    if not os.path.exists(genesisjson):
        raise MCError(
            ' genesis.json not exist, dir path is %s' % dir)
    if not os.path.exists(bootstrapnodesjson):
        raise MCError(
            ' bootstrapnodes.json not exist, dir path is %s' % dir)

    chain = cc.get_chain()
    port = cc.get_port()
    chain_id = chain.get_id()
    chain_version = chain.get_version()

    # parser fisco-bcos version and check it.
    fisco = Fisco(fisco_path)
    logger.debug(' fisco is %s', fisco)

    acp = AllChainPort()
    # port check
    for node in cc.get_nodes():
        for index in range(node.get_node_num()):
            # create dir for every node on the server
            acp.port_conflicts_outside_chain(chain.get_id(), node.get_host_ip(), port.to_port(index))
            acp.port_conflicts_inside_chain(node.get_host_ip(), port.to_port(index) ,chain.get_id(), chain.get_version())

    try:
        # create host dir
        os.makedirs(chain.data_dir())
        # copy genesis.json bootstrapnodes.json to chain dir.
        shutil.copy(genesisjson, chain.data_dir() + '/')
        shutil.copy(bootstrapnodesjson, chain.data_dir() + '/')

        # create common dir
        build_chain.build_common_dir(chain, fisco)

        # build install dir for every server
        for node in cc.get_nodes():
            build_chain.expand_host_dir(chain, node, port, fisco)

    except Exception as e:
        if os.path.exists(chain.data_dir()):
            shutil.rmtree(chain.data_dir())
        logger.error(' expand failed, chain id is %s, chain version is %s, exception is %s.',
                     chain_id, chain_version, e)
        raise MCError(' expand failed, chain id is %s, chain version is %s, exception is %s' % (
            chain_id, chain_version, e))