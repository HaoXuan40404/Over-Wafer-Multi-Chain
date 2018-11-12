#coding:utf-8
import os
import sys
import shutil
from pys.log import logger
from pys.tool import utils
from pys.data_mgr.port import HostPort
from pys.data_mgr.port import ChainVerPort
from pys.conf.build_chain_conf import NodeEle


def web3_conf_by_chain(chain, gm=False, web3_conf_path=None):

    cvp = ChainVerPort(chain.get_id(), chain.get_version())

    web3_connect_nodes_list = ''
    for host, hp in cvp.get_ports().items():
        for node, port in hp.get_ports().items():
            web3_connect_nodes_list += ('<value>%s_%s@%s:%d</value>' %
                                        (host, node, host, port.get_channel_port()))

    if (web3_conf_path is None) or (not os.path.exists(web3_conf_path)):
        if gm:
            shutil.copy(chain.data_dir() + '/' + 'common/web3sdk/conf/applicationContext_GM.xml',
                        chain.data_dir() + '/' + 'common/web3sdk/conf/applicationContext.xml')
        else:
            shutil.copy(chain.data_dir() + '/' + 'common/web3sdk/conf/applicationContext_NB.xml',
                        chain.data_dir() + '/' + 'common/web3sdk/conf/applicationContext.xml')
        web3_conf_path = chain.data_dir() + '/' + 'common/web3sdk/conf/applicationContext.xml'

    logger.info('  web3sdk config file is %s', web3_conf_path)

    return utils.replace(web3_conf_path, 'WEB3SDK_NODES_LIST',
                         web3_connect_nodes_list)
