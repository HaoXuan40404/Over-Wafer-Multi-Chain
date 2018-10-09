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
from pys.node import temp_node
from pys.node.bootstrapsnode import P2pHosts
from pys.node.bootstrapsnode import P2pHost

def chain_expand(cfg, package_path):
    """解析配置构建区块链对应版本的安装包

    Arguments:
        cfg {string} -- 配置信息, 可以是一个单独的配置文件或者是包含多个配置文件的目录, 例如：./conf/config.conf or ./conf
        package_path {string} -- 指定的存放安装包的路径
    Returns:
        无返回
    """
    logger.debug('expand cfg is %s, package_path is %s ', cfg, package_path)

    
    # 判断package_path是否存在
    if not (os.path.exists(package_path)):
        consoler.error(
            ' package_path is not exist, input path is %s', package_path)
        return

    # 通过cfg里的chain_id:version得到fisco-bcos

    path.set_fiso_path(package_path)
    fisco_path = path.get_fisco_path

    cc_dict = {}
    if os.path.exists(cfg) and os.path.isfile(cfg):

        consoler.info('config file is %s, fisco bcos path is %s' %
                      (cfg, fisco_path))
         # 单个配置文件解析
    elif os.path.isdir(cfg):

        consoler.info('\t config dir is %s, fisco bcos path is %s' %
                      (cfg, fisco_path))
        # 指定文件夹, 解析文件夹中的所有配置文件, 解析失败则跳过

    logger.debug('build cfg end.')



def expand_cfg(cc):
    """根据配置对象构建一条区块链的安装包

    Arguments:
        cc {ConfigConf} -- 解析配置文件生成ConfigConf对象   

    Raises:
        Exception
    """
    logger.info('expand, cc is %s', cc)

    dir = data.package_dir(cc.get_chain().get_id(),
                           cc.get_chain().get_version())
    port = cc.get_port()
    chain = cc.get_chain()

    consoler.info('\t\t build install package for chain %s version %s',
                  cc.get_chain().get_id(), cc.get_chain().get_version())

    # 创建新文件夹 或者在该目录下创建新的安装包？
    
    # 拷贝bootstrapsnode.json

    # 拷贝genesis.json文件到各个文件夹

    # 拷贝fisco-bcos文件

    # web3sdk
