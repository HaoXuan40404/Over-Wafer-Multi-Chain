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


def common_build(dir):
    """build common directory for version of the chain
    
    Arguments:
        dir {string} -- create the directory for the common directory

    common/
        ├── check.sh
        ├── fisco-bcos
        ├── monitor.sh
        ├── node_manager.sh
        ├── register.sh
        ├── rmlogs.sh
        ├── scripts
        ├── start.sh
        ├── stop.sh
        ├── unregister.sh
        └── web3sdk
    """
    # create common dir
    com_dir = dir + '/common'
    os.makedirs(com_dir)

    # copy fisco-bcos file
    shutil.copy(path.get_fisco_path(), com_dir)

    # web3sdk
    shutil.copytree(path.get_path() + '/tpl/web3sdk', dir + '/web3sdk')
    # copy ca.crt to web3sdk conf dir
    shutil.copy(ca.get_agent_ca_path() + '/sdk/ca.crt',
                com_dir + '/web3sdk/conf')
    # copy client.keystore to web3sdk conf dir
    shutil.copy(ca.get_agent_ca_path() + '/sdk/client.keystore',
                com_dir + '/web3sdk/conf')

    # copy scripts to common dir
    shutil.copy(path.get_path() + '/scripts/node/start.sh', com_dir)
    shutil.copy(path.get_path() + '/scripts/node/stop.sh', com_dir)
    shutil.copy(path.get_path() + '/scripts/node/check.sh', com_dir)
    shutil.copy(path.get_path() + '/scripts/node/register.sh', com_dir)
    shutil.copy(path.get_path() + '/scripts/node/unregister.sh', com_dir)
    shutil.copy(path.get_path() + '/scripts/node/monitor.sh', com_dir)
    shutil.copy(path.get_path() + '/scripts/node/rmlogs.sh', com_dir)
    shutil.copy(path.get_path() + '/scripts/node/node_manager.sh', com_dir)

    # copy scripts dir to common dir
    shutil.copytree(path.get_path() + '/scripts', com_dir + '/scripts')

def chain_build(cfg, fisco_path):
    """parser input config file, build install pacakge by 

    Arguments:
        cfg {string} -- 配置信息, 可以是一个单独的配置文件或者是包含多个配置文件的目录, 例如：./conf/config.conf or ./conf
        fisco_path {string} -- 指定的fisco-bcos的路径, 例如：/usr/local/bin/fisco-bcos
    Returns:
        无返回
    """

    logger.debug('build cfg is %s, fisco is %s ', cfg, fisco_path)

    # check if fisco-bcos exists
    if not (os.path.exists(fisco_path) and os.path.isfile(fisco_path)):
        consoler.error(
            ' fisco-bcos is not exist, input path is %s', fisco_path)
        return

    path.set_fiso_path(fisco_path)

    cc_dict = {}
    if os.path.exists(cfg) and os.path.isfile(cfg):

        consoler.info('config file is %s, fisco bcos path is %s' %
                      (cfg, fisco_path))
        # 单个配置文件解析
        try:
            cc = parser.do_parser(cfg)
            consoler.info('parser config %s successs, chain_id is %s, chain_version is %s' % (
                cfg, cc.get_chain().get_id(), cc.get_chain().get_version()))

            key = cc.get_chain().get_id() + '_' + cc.get_chain().get_version()
            cc_dict[key] = cc

        except Exception as e:
            consoler.error(
                'invalid config format parser failed, config is %s, excption is %s', cfg, e)
            logger.warn('parser cfg %s end exception, e is %s ', cfg, e)

    elif os.path.isdir(cfg):

        consoler.info('\t config dir is %s, fisco bcos path is %s' %
                      (cfg, fisco_path))
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
                    consoler.error(
                        'chain_id %s and chain_version %s config repeat, please update the chain_version.',cc.get_chain(
                    ).get_id(), cc.get_chain().get_version())
                    break
                else:
                    consoler.info('\t parser config %s successs, chain_id is %s, chain_version is %s' % (
                        cfg, cc.get_chain().get_id(), cc.get_chain().get_version()))
                    cc_dict[key] = cc
            except Exception as e:
                consoler.error(
                    'skip config %s, invalid config format parser failed, exception is %s', c, e)
                logger.warn('parser cfg %s end exception, e %s ', c, e)

    else:
        consoler.error(
            'invalid config, neither directory nor file, config is %s', cfg)

    logger.info('cc_dict is %s', cc_dict)

    # 构建所有链的安装包
    if len(cc_dict) != 0:
        for cc in cc_dict.itervalues():
            build_cfg(cc)
    else:
        consoler.info(' build operation will do nothing.')

    logger.debug('build cfg end.')


def build_cfg(cc):
    """build all install package for one chain base on cc 

    Arguments:
        cc {ConfigConf} -- ConfigConf object  

    Raises:
        Exception -- exception description
    """

    logger.info('building, cc is %s', cc)

    dir = data.package_dir(cc.get_chain().get_id(),
                           cc.get_chain().get_version())
    port = cc.get_port()
    chain = cc.get_chain()

    consoler.info('\t\t build install package for chain %s version %s',
                  cc.get_chain().get_id(), cc.get_chain().get_version())

    # create dir base on version of the chain.
    if os.path.isdir(dir):
        logger.warn('version of this chain already exists chain is %s, version is %s',
                    cc.get_chain().get_id(), cc.get_chain().get_version())

        consoler.error(' build install package for chain %s version %s failed, version data aleady exist, please change the version of the chain!!!.',
                       cc.get_chain().get_id(), cc.get_chain().get_version())

        return

    os.makedirs(dir)

    try:
        # generate bootstrapsnode.json
        phs = P2pHosts()
        for node in cc.get_nodes():
            for index in range(node.get_node_num()):
                phs.add_p2p_host(
                    P2pHost(node.get_p2p_ip(), cc.get_port().get_p2p_port() + index))
        with open(dir + '/bootstrapnodes.json', "w+") as f:
            f.write(phs.to_json())

        # create common dir
        common_build(dir)

        # create temp node for export genesis.json file
        temp_node.temp_node_build(dir, port)

        # start temp node
        if not temp_node.start_temp_node(dir, port):
            raise Exception('temp node start failed.')

        # build install dir for every server
        for node in cc.get_nodes():
            build.build_install_dir(dir, chain, port, node, temp_node)

        # stop temp node
        temp_node.stop_temp_node(dir)

        # export genesis.json file from the temp node
        if not temp_node.export_genesis(dir):
            raise Exception('export genesis.json failed.')

        temp_node.clean_temp_node(dir)

        # copy genesis.json bootstrapnodes.json
        for node in cc.get_nodes():
            for index in range(node.get_node_num()):
                shutil.copy(dir + '/genesis.json', dir +
                            ('/%s/node%d/' % (node.get_host_ip(), index)))
                shutil.copy(dir + '/bootstrapnodes.json', dir +
                            ('/%s/node%d/' % (node.get_host_ip(), index)))

        utils.replace(dir + '/web3sdk/conf/applicationContext.xml',
                      'NODE@HOSTIP', 'node0@127.0.0.1:%d' % port.get_channel_port())

        logger.info('build end ok, chain is %s', chain)
        consoler.info('\t\t build install package for chain %s version %s success.',
                      cc.get_chain().get_id(), cc.get_chain().get_version())

    except Exception as e:
        consoler.error('\t\t build install package for chain %s version %s failed, exception is %s',
                       cc.get_chain().get_id(), cc.get_chain().get_version(), e)

        temp_node.clean_temp_node(dir)
        if os.path.isdir(dir):
            shutil.rmtree(dir)
