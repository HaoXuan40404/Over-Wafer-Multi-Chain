# coding:utf-8

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
from pys.node.bootstrapsnode import P2pHosts
from pys.node.bootstrapsnode import P2pHost


def chain_build(cfg, fisco_path):
    """解析配置构建区块链对应版本的安装包

    Arguments:
        cfg {string} -- 配置信息, 可以是一个单独的配置文件或者是包含多个配置文件的目录, 例如：./conf/config.conf or ./conf
        fisco_path {string} -- 指定的fisco-bcos的路径, 例如：/usr/local/bin/fisco-bcos
    Returns:
        无返回
    """

    logger.debug('build cfg is %s, fisco is %s ', cfg, fisco_path)

    # 判断fisco-bcos文件是否存在
    if not (os.path.exists(fisco_path) and os.path.isfile(fisco_path)):
        consoler.info('\t [ERROR] fisco-bcos is not exist, path is %s', fisco_path)
        return 

    path.set_fiso_path(fisco_path)

    cc_dict = {}
    if os.path.exists(cfg) and os.path.isfile(cfg):

        consoler.info('\t config file is %s, fisco bcos path is %s' % (cfg, fisco_path))
        # 单个配置文件解析
        try:
            cc = parser.do_parser(cfg)
            consoler.info('\t parser config %s successs, chain_id is %s, chain_version is %s' % (cfg, cc.get_chain().get_id(), cc.get_chain().get_version()))
            key = cc.get_chain().get_id() + '_' + cc.get_chain().get_version()
            cc_dict[key] = cc
        except Exception as e:
            consoler.info('\t [ERROR] invalid config format parser failed, config is %s, exp is %s', cfg, e)
            logger.warn('parser cfg %s end exception, e is %s ', cfg, e)

    elif os.path.isdir(cfg):

        consoler.info('\t config dir is %s, fisco bcos path is %s' % (cfg, fisco_path))
        # 指定文件夹, 解析文件夹中的所有配置文件, 解析失败则跳过
        for c in os.listdir(cfg):
            try:
                logger.debug('dir is %s, cfg is %s', cfg, c)
                cc = parser.do_parser(cfg + '/' + c)

                key = cc.get_chain().get_id() + '_' + cc.get_chain().get_version()
                # 配置重复
                if key in cc_dict:
                    logger.error('chain_id and chain_version duplicate, chain_id is %s, chain_version is %s', cc.get_chain(
                    ).get_id(), cc.get_chain().get_version())
                    cc_dict = {}
                    consoler.info('\t [ERROR] chain_id %s and chain_version %s config repeat.')
                    break
                else:
                    consoler.info('\t parser config %s successs, chain_id is %s, chain_version is %s' % (cfg, cc.get_chain().get_id(), cc.get_chain().get_version()))
                    cc_dict[key] = cc
            except Exception as e:
                consoler.info('\t [ERROR] skip config %s, invalid config format parser failed, exp is %s', c, e)
                logger.warn('parser cfg %s end exception, e %s ', c, e)

    else:
        consoler.info('\t [ERROR] invalid config, neither directory nor file, config is %s', cfg)

    logger.info('cc_dict is %s', cc_dict)

    # 构建所有链的安装包
    if len(cc_dict) != 0:
        for cc in cc_dict.itervalues():
            build_cfg(cc)

    logger.debug('build cfg end.')


def build_cfg(cc):
    """根据配置对象构建一条区块链的安装包

    Arguments:
        cc {ConfigConf} -- 解析配置文件生成ConfigConf对象   

    Raises:
        Exception
    """

    logger.info('building, cc is %s', cc)

    dir = data.package_dir(cc.get_chain().get_id(),
                           cc.get_chain().get_version())
    port = cc.get_port()
    chain = cc.get_chain()

    consoler.info('\t\t build install package for chain %s version %s', cc.get_chain().get_id(), cc.get_chain().get_version())

    # 创建文件夹
    if os.path.isdir(dir):
        logger.warn('version of this chain already exists chain is %s, version is %s',
                    cc.get_chain().get_id(), cc.get_chain().get_version())
        
        consoler.info('\t\t [ERROR] build install package for chain %s version %s failed, data dir aleady exist', cc.get_chain().get_id(), cc.get_chain().get_version())
        
        return
    os.makedirs(dir)

    try:
        # 生成bootstrapsnode.json
        phs = P2pHosts()
        for node in cc.get_nodes():
            for index in range(node.get_node_num()):
                phs.add_p2p_host(
                    P2pHost(node.get_p2p_ip(), cc.get_port().get_p2p_port() + index))
        with open(dir + '/bootstrapnodes.json', "w+") as f:
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
                shutil.copy(dir + '/genesis.json', dir +
                            ('/%s/node%d/' % (node.get_host_ip(), index)))

        logger.info('build end ok.')
        consoler.info('\t\t build install package for chain %s version %s success.', cc.get_chain().get_id(), cc.get_chain().get_version())

    except Exception as e:
        logger.warn('build end exception, e is %s', e)
        consoler.info('\t\t build install package for chain %s version %s failed, exp is %s', cc.get_chain().get_id(), cc.get_chain().get_version(), e)

        temp_node.clean_temp_node(dir)
        if os.path.isdir(dir):
            shutil.rmtree(dir)
