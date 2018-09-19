#coding:utf-8

import os
import sys
import shutil

from pys import path
from pys import utils
from pys.log import logger
from pys.chain import parser
from pys.chain import data
from pys.node import build
from pys.node import temp_node
from pys.node.bootstrapsnode import P2pHosts
from pys.node.bootstrapsnode import P2pHost

def chain_build(cfg, fisco_path):
    '''
    解析config.conf配置并且构建区块链的安装包
    '''
    logger.info('building, cfg is %s', cfg)
    logger.info('building, fisco bcos path is %s', fisco_path)

    path.set_fiso_path(fisco_path)

    # 配置解析
    try:
        cc = parser.do_parser(cfg)
    except Exception as e:
        logger.warn('parser cfg end exception, e = ' + e)
        return 

    dir = data.package_dir(cc.get_chain().get_id(), cc.get_chain().get_version())
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

        for node in cc.get_nodes():
            for index in range(node.get_node_num()):
                phs.add_p2p_host(P2pHost(node.get_p2p_ip(), cc.get_port().get_p2p_port() + index))
        with open(dir + '/bootstrapnodes.json',"w+") as f:
            f.write(phs.to_json())
        
        temp_node.temp_node_build(dir, port)

        if not temp_node.start_temp_node(dir):
            logger.warn('start temp node failed.')
            raise Exception('temp node start failed')

        # 构建各个安装包
        for node in cc.get_nodes():
            build.build_install_dir(dir, chain, port, node, temp_node)
        
        temp_node.stop_temp_node(dir)
        temp_node.export_genesis(dir)
        temp_node.clean_temp_node(dir)

        # 拷贝genesis.json文件到各个文件夹
        for node in cc.get_nodes():
            index = 0
            while index < node.get_node_num():
                shutil.copy(dir + '/genesis.json', dir + ('/%s/node%d/' % (node.get_host_ip(), index)) )
                index += 1

        logger.info('build end ok.')

    except Exception as e:
        logger.warn('build end exception, e is %s', e)
        if os.path.isdir(dir):
            shutil.rmtree(dir)
    


    