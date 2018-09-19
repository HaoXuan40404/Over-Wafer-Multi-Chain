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
    解析cfg_dir中的所有的链的配置并且构建区块链的安装包
    '''

    path.set_fiso_path(fisco_path)

    cc_list = []
    if os.path.exists(cfg):
        # 指定单个配置文件解析
        try:
            cc = parser.do_parser(cfg)
            cc_list.append(cc)
        except Exception as e:
            print('parser %s failed , skip ...', cfg)
            logger.warn('parser cfg %s end exception, e is %s ', cfg, e)

    elif os.path.isdir(cfg):
        # 指定文件夹, 解析文件夹中的所有配置文件, 解析失败则跳过
        for c in os.listdir(cfg):
            try:
                logger.debug('dir is %s, cfg is %s', cfg, c)
                cc = parser.do_parser(cfg + '/' + c)
                cc_list.append(cc)
            except Exception as e:
                print('parser %s failed, skip ...', c)
                logger.warn('parser cfg %s end exception, e %s ', c, e)

    else:
        # 指定的参数即不是目录也不是配置 
        print('unkown cfg path , cfg is %s ', cfg)
        logger.warn('unkown cfg path , cfg is %s', cfg)
    
    logger.info('cc_list is %s', cc_list)

    # 构建所有链的安装包
    for cc in cc_list:
        __build(cc)

def __build(cc):
    '''
    解析config.conf配置并且构建区块链的安装包
    '''
    logger.info('building, cc is %s', cc)

    dir = data.package_dir(cc.get_chain().get_id(), cc.get_chain().get_version())
    port = cc.get_port()
    chain = cc.get_chain()
    # 创建文件夹
    if os.path.isdir(dir):
        logger.warn('version of this chain already exists chain is %s, version is %s', cc.get_chain().get_id(), cc.get_chain().get_version())
        return 
    os.makedirs(dir)

    try:
        # 生成bootstrapsnode.json
        phs = P2pHosts()
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
            for index in range(node.get_node_num()):
                shutil.copy(dir + '/genesis.json', dir + ('/%s/node%d/' % (node.get_host_ip(), index)) )

        logger.info('build end ok.')

    except Exception as e:
        logger.warn('build end exception, e is %s', e)
        temp_node.clean_temp_node(dir)
        if os.path.isdir(dir):
            shutil.rmtree(dir)
    


    