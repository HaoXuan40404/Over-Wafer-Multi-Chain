#coding:utf-8
import os
import sys
import shutil

from pys import path
from pys.tool import utils
from pys.tool.java import JAVA
from pys.log import logger
from pys.log import consoler
from pys.conf import build_chain_conf
from pys.build import expand_chain
from pys.error.exp import MCError
from pys.data_mgr.names import Names
from pys.conf.build_chain_conf import ConfigConf

def expand(cfg, dir):
    """expand operation 
    
    Arguments:
        cfg {string} -- config file path
        dir {string} -- dir with fisco-bcos, genesis.json, bootstrapsnode.json
    """

    logger.debug(' cfg is %s, dir is %s', cfg, dir)

    try:

        # check java env
        java = JAVA()
        
        try:
            # parser and check config if valid
            cc = ConfigConf(cfg)
        except Exception as e:
            raise MCError(
                ' parser config failed, invalid format, config is %s, exception is %s' % (cfg, e))

        if os.path.exists(cc.get_chain().data_dir()):
            ns = Names()
            expand_chain.expand_on_exist_chain(cc)
            ns.write()
        else:
            expand_chain.expand_on_nonexist_chain(cc, dir)
        
        consoler.info(' expand install package for chain %s version %s success.', cc.get_chain().get_id(), cc.get_chain().get_version())

    except MCError as me:
        consoler.error(me)
        consoler.error(' \033[1;31m \t %s \033[0m', me)
