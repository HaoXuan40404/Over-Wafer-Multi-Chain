# coding:utf-8

import os
import sys
import shutil

from pys.log import logger
from pys.log import consoler
from pys.tool.java import JAVA
from pys.conf.build_chain_conf import ConfigConfs
from pys.data_mgr.names import Names
from pys.error.exp import MCError
from pys.fisco.version import Fisco


def build(cfg, fisco_path):
    """parser input config file, build install pacakge by 

    Arguments:
        cfg {string} --config, maybe a config.json or a dictionary of conf,eg: ./conf/config.conf or ./conf
        fisco_path {string} -- path of fisco-bcos, eg: /usr/local/bin/fisco-bcos
    """

    logger.info('build cfg is %s, fisco is %s ', cfg, fisco_path)
    try:
        # parser fisco-bcos version and check it.
        fisco = Fisco(fisco_path)
        if not fisco.is_13_version():
            logger.error(
                ' fisco-bcos is not 1.3.x version, not support now, %s', fisco)
            raise MCError(
                ' fisco-bcos is not 1.3.x version, not support now, %s' % fisco)
        
        # check java env
        java = JAVA()

        # parser and check config if valid
        ccs = ConfigConfs(cfg).get_ccs()
        ns = Names()
        nsc = 0
        # build all chain
        if len(ccs) != 0:
            for cc in ccs.values():
                try:
                    chain_id = cc.get_chain().get_id()
                    chain_version = cc.get_chain().get_version()
                    chain_name = cc.get_chain().get_name()
                    consoler.info(
                        ' build install package for chain %s version %s.', chain_id, chain_version)
                    build_cfg(cc, fisco)
                    if ns.append(chain_id, chain_name):
                        nsc = nsc + 1
                    consoler.info(
                        ' \t build install package for chain %s version %s success.', chain_id, chain_version)
                except MCError as me:
                    logger.error(me)
                    consoler.error(' \033[1;31m \t %s \033[0m', me)
                    
            if nsc > 0:
                ns.write()
        else:
            consoler.info(' build operation will do nothing.')

    except MCError as me:
        logger.error(me)
        consoler.error(me)

    logger.info(' chain build end.')
    