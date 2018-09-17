#coding:utf-8

import os
import sys
import shutil

from pys import path
from pys import utils
from data import Data
from pys.log import logger
from pys.chain import parser
from pys.node import build
from pys.node import temp_node
from pys.node.bootstrapsnode import P2pHosts
from pys.node.bootstrapsnode import P2pHost

def chain_build(cfg):
    '''
    解析config.conf配置并且构建区块链的安装包
    '''
    logger.info('building, cfg is %s', cfg)

    # 配置解析
    try:
        cc = parser.do_parser(cfg)
    except Exception as e:
        logger.warn('parser cfg end exception, e = ' + e)
        return 

    dir = Data().dir(cc.get_chain().get_id(), cc.get_chain().get_version())
    port = cc.get_port()
    chain = cc.get_chain()
    # 创建文件夹
    if os.path.isdir(dir):
        logger.warn('dir already exist, dir is ' + dir)
        return 
    os.makedirs(dir)

    try:
        phs = P2pHosts()
        # 生成bootstrapsnode.json
        node_json_lists = []
        for node in cc.get_nodes():
            for index in range(node.get_node_num()):
                phs.add_p2p_host(P2pHost(node.get_p2p_ip(), cc.get_port().get_p2p_port() + index))
                node_json_lists.append(dir + '/' + node.get_host_ip() + ('/node%d' % index) + '/data/node.json')
        with open(dir + '/bootstrapnodes.json',"w+") as f:
            f.write(phs.to_json())
        
        # 构建各个安装包
        for node in cc.get_nodes():
            build.build_install_dir(dir, chain, port, node)

        # 构建temp节点
        temp_node.temp_node_build(dir, port)
        if temp_node.start_temp_node(dir):
            for nodejson in node_json_lists:
                temp_node.registerNode(dir, nodejson)
<<<<<<< HEAD
            #export genssis.json   
=======
            temp_node.stop_temp_node(dir)
            temp_node.export_genesis(dir)
>>>>>>> 7c968de4fff33f03d07a667016ac805fe6314704
            temp_node.clean_temp_node(dir)
        else:
            raise Exception('temp node start failed')
        
        logger.info('build end ok.')

    except:
        logger.warn('build end exception')
        if os.path.isdir(dir):
            shutil.rmtree(dir)
    


    