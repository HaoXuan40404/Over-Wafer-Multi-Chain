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
from pys.exp import MCError
from pys.node.bootstrapsnode import P2pHosts
from pys.node.bootstrapsnode import P2pHost

def common_build(dir):
    """build common directory for version of the chain
    
    Arguments:
        dir {string} -- create the directory

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
    shutil.copytree(path.get_path() + '/tpl/web3sdk', com_dir + '/web3sdk')
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

    logger.debug(' build_common end, dir is %s ', dir)

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

        consoler.info('\t config file is %s, fisco bcos path is %s' %
                      (cfg, fisco_path))
        # single input config
        try:
            cc = parser.do_parser(cfg)
            chain = cc.get_chain()
            consoler.info('\t parser config %s successs, chain_id is %s, chain_version is %s' % (
                cfg, chain.get_id(), chain.get_version()))

            key = chain.get_id() + '_' + chain.get_version()
            cc_dict[key] = cc

        except Exception as e:
            consoler.error(
                ' invalid config format parser failed, config is %s, excption is %s', cfg, e)
            logger.warn('parser cfg %s end exception, e is %s ', cfg, e)

    elif os.path.isdir(cfg):

        consoler.info('\t config dir is %s, fisco bcos path is %s' %
                      (cfg, fisco_path))
        # The input config is in the folder 
        for c in os.listdir(cfg):
            try:
                logger.debug('dir is %s, cfg is %s', cfg, c)
                cc = parser.do_parser(cfg + '/' + c)
                key = cc.get_chain().get_id() + '_' + cc.get_chain().get_version()
                # config repeat.
                if key in cc_dict:
                    logger.error('chain_id and chain_version duplicate, chain_id is %s, chain_version is %s', cc.get_chain(
                    ).get_id(), cc.get_chain().get_version())
                    ## clear cc_dict and will exit.
                    cc_dict = {}
                    consoler.error(
                        'chain_id %s and chain_version %s config repeat, please update the chain_version.', cc.get_chain(
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

    # build all chain
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

    port = cc.get_port()
    chain = cc.get_chain()
    dir = chain.data_dir()

    consoler.info('\t build install package for chain %s version %s',
                  chain.get_id(), chain.get_version())

    # create dir base on version of the chain.
    if os.path.isdir(dir):
        logger.warn(' version of this chain already exists chain is %s, version is %s',
                    cc.get_chain().get_id(), cc.get_chain().get_version())

        consoler.error(' build chain %s version %s failed, chain aleady exist, please change the version of the chain!!!.',
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
            raise MCError(' temp node start failed.')

        # build install dir for every server
        for node in cc.get_nodes():
            build.build_host_dir(chain, node, port, temp_node)

        # stop temp node
        temp_node.stop_temp_node(dir)

        # export genesis.json file from the temp node
        if not temp_node.export_genesis(dir):
            raise MCError(' export genesis.json failed.')

        temp_node.clean_temp_node(dir)

        # copy genesis.json bootstrapnodes.json
        for node in cc.get_nodes():
            for index in range(node.get_node_num()):
                shutil.copy(dir + '/genesis.json', dir + '/' + node.get_host_ip() + '/node' + str(index))

        utils.replace(dir + '/common/web3sdk/conf/applicationContext.xml',
                      'NODE@HOSTIP', 'node0@127.0.0.1:%d' % port.get_channel_port())

        logger.info(' build end ok, chain is %s', chain)
        consoler.info('\t build install package for chain %s version %s success.',
                      cc.get_chain().get_id(), cc.get_chain().get_version())

    except Exception as e:
        consoler.error('\t build install package for chain %s version %s failed, exception is %s',
                       cc.get_chain().get_id(), cc.get_chain().get_version(), e)

        temp_node.clean_temp_node(dir)
        if os.path.isdir(dir):
            shutil.rmtree(dir)

def expand_cc(cc, fisco_path, genesisjson, bootstrapnodesjson):

    chain = cc.get_chain()
    port = cc.get_port()

    if os.path.exists(chain.data_dir()): 
        # expand on exist chain, check common、 genesis.json、 bootstrapnodes.json file exist.
        if not os.path.exists(chain.data_dir() + '/common'):
            raise MCError(' chain dir exist ,but common dir not exist, chain_id %s and chain_version %s' % (chain.get_id(), chain.get_version()))
        if not os.path.exists(chain.data_dir() + '/genesis.json'):
            raise MCError(' chain dir exist ,but genesis.json not exist, chain_id %s and chain_version %s' % (chain.get_id(), chain.get_version()))
        if not os.path.exists(chain.data_dir() + '/bootstrapnodes.json'):
            raise MCError(' chain dir exist ,but bootstrapnodes.json not exist, chain_id %s and chain_version %s' % (chain.get_id(), chain.get_version()))
        
        # expand install dir for every server
        for node in cc.get_nodes():
            try:
                build.expand_host_dir(chain, node, port)
            except Exception as e:
                continue
    else:
        try:
            # check if fisco-bcos、genesis.json、bootstrapsnode.json exist.
            if not os.path.exists(fisco_path):
                raise MCError(
                    ' fisco bcos not exist, fisco bcos path is %s' % fisco_path)
            if not os.path.exists(genesisjson):
                raise MCError(
                    ' genesis.json not exist, genesis.json path is %s' % genesisjson)
            if not os.path.exists(bootstrapnodesjson):
                raise MCError(
                    ' bootstrapnodes.json not exist, bootstrapnodes.json path is %s' % bootstrapnodesjson)

            os.makedirs(chain.data_dir())
            path.set_fiso_path(fisco_path)
            shutil.copy(genesisjson, chain.data_dir() + '/')
            shutil.copy(bootstrapnodesjson, chain.data_dir() + '/')

            # create common dir
            common_build(chain.data_dir())
            # build install dir for every server
            for node in cc.get_nodes():
                build.expand_host_dir(chain, node, port)

        except Exception as e:
            if os.path.exists(chain.data_dir()):
                shutil.rmtree(chain.data_dir())
            logger.error(' expand failed, chain id is %s, chain version is %s, exception is %s.',
                         chain.get_id(), chain.get_version(), e)
        else:
            consoler.info('\t expand package for chain %s version %s success.',
                          chain.get_id(), chain.get_version())

    logger.info('expand end, cc is %s', cc)
    

def chain_expand(args):
    """expand operation 
    
    Arguments:
        cfg {string} -- config file path
        fisco_path {string} -- fisco-bcos file path
        genesisjson {string} -- genesis.json file path
        bootstrapnodesjson {string} -- bootstrapsnodes.json file path
    """

    if len(args) < 2:
        consoler.error(' expand operation at least need 2 parameters !!! ')
        return 

    cfg = args[0]
    fisco_path = args[1]
    if len(args) > 2:
        genesisjson = args[2]
    else:
        genesisjson = ''
    if len(args) > 3:
        bootstrapnodesjson = args[3]
    else:
        bootstrapnodesjson = ''

    try:
        # parser config file
        cc = parser.do_parser(cfg)
        chain = cc.get_chain()
        consoler.info(' parser config %s success, chain_id is %s, chain_version is %s' % (
            cfg, chain.get_id(), chain.get_version()))
        logger.info('expand operation, parser config success, cc is %s', cc)

    except Exception as e:
        consoler.error(
            'invalid config format parser failed, config is %s, exception is %s', cfg, e)
    else:
        expand_cc(cc, fisco_path, genesisjson, bootstrapnodesjson)
        
    

