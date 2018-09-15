#coding:utf-8

import os
import sys

from pys import path
from pys import utils
from data import Data
from pys.log import logger
from pys.chain import parser
from pys.node import node_build
from pys.node.bootstrapsnode import P2pHosts
from pys.node.bootstrapsnode import P2pHost

def build(cfg):
    '''
    解析config.conf配置并且构建区块链的安装包
    '''
    logger.info('building, cfg is %s', cfg)
    try:
        # 配置解析
        cc = parser.do_parser(cfg)

        dir = Data().dir(cc.get_chain().get_id(), cc.get_chain().get_version())
        port = cc.get_port()
        chain = cc.get_chain()

        # 创建文件夹
        if not os.path.isdir(dir):
            os.makedirs(dir)

        phs = P2pHosts()
        for node in cc.get_nodes():
            # 生成bootstrapsnode.json
            for index in range(node.get_node_num()):
                phs.add_p2p_host(P2pHost(node.get_p2p_ip(), cc.get_port().get_p2p_port() + index))
                # 为每个节点分配ca
                # add soon
        with open(dir + '/bootstrapnodes.json',"w+") as f:
            f.write(phs.to_json())
        
        # 构建各个安装包
        for node in cc.get_nodes():
            node_build.build_install_dir(dir, chain, port, node)
    except:
        pass
        
    logger.info('build end.')
    


    