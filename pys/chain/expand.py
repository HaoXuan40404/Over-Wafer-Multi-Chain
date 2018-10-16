# coding:utf-8

import os
import sys
import shutil

from pys import path
from pys import utils
from pys import ca
from pys.log import logger
from pys.log import consoler
from pys.chain import parser
from pys.chain import data
from pys.node import build
from pys.node.bootstrapsnode import P2pHosts
from pys.node.bootstrapsnode import P2pHost

def chain_expand(cfg, fisco_bcos, genesis, bootstrapnodes):
    
    logger.debug('expand cfg is %s, fisco-bcos is %s, genesis is %s, bootstrpanodes is %s ',
                 cfg, fisco_bcos, genesis, bootstrapnodes)

    try:
        # parse config
        cc = parser.do_parser(cfg)
        consoler.info('parser config %s successs, chain_id is %s, chain_version is %s' % (
            cfg, cc.get_chain().get_id(), cc.get_chain().get_version()))

    except Exception as e:
        # exception throw, config maybe invalid format.
        consoler.error(
            'invalid config format parser failed, config is %s, excption is %s', cfg, e)
        return

    # check if install package of the server already exist.
    dir = cc.get_chain().data_dir()
    if os.path.exists(dir):
        # package already exist, expand operation on chain which already has install package.
        expand_add_package(cc, fisco_bcos, genesis, bootstrapnodes)
    else:
        # 
        expand_add_node(cc) 

    logger.info('expand end.')

def expand_add_package(cc, fisco_bcos, genesis, bootstrapnodes):

    # check if fisco-bcos exists
    if not (os.path.exists(fisco_bcos) and os.path.isfile(fisco_bcos)):
        consoler.error(' fisco-bcos is not exist, path is %s', fisco_bcos)
        return

    # check if genesis.json file exists
    if not (os.path.exists(genesis) and os.path.isfile(genesis)):
        consoler.error(' genesis.json is not exist, path is %s', genesis)
        return

    # check if bootstrapsnode.json file exists
    if not (os.path.exists(bootstrapnodes) and os.path.isfile(bootstrapnodes)):
        consoler.error(' bootstrapnodes.json is not exist, path is %s', bootstrapnodes)
        return
    
    path.set_fiso_path(fisco_bcos)

    dir = cc.get_chain().data_dir()

    # build install package dir
    os.makedirs(dir)
    shutil.copy(path.get_path() + '/scripts/node/start.sh', node_dir)
    shutil.copy(path.get_path() + '/scripts/node/start.sh', node_dir)
    build.build_install_dir(dir, cc.get_chain(), cc.get_port(), cc.get_nodes(), None)


def expand_add_node(cc):
    pass
