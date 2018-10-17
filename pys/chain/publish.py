# coding:utf-8
import os
from pys import utils
from pys import ansible
from pys.log import logger
from pys.log import consoler
from pys.chain import meta
from pys.chain import data
from pys.chain.chain import Chain
from pys.node import config

from pys.chain.chain import Chain


def publish_chain(chains):
    """发布命令行传入的所有指定版本的区块链.
    
    Arguments:
        list_chain_version {list} -- 需要发布的链, 格式为chain_id:chain_version, 可以一次发布多个, 多个之间使用空格分离.
    
    Returns:
        无返回
    """
    pchains = []
    for i in range(len(chains)):
        chain = chains[i].split(':')
        if len(chain) != 2:
            logger.error('not chain_id:chain_version format, str is %s', chains[i])
            consoler.error('skip, invalid publish format, chain_id:chain_version should require, chain is %s', chain)
            continue

        chain_id = chain[0]
        chain_version = chain[1]

        pchains.append(Chain(chain_id, chain_version))
        # consoler.info('\t append publish chain, chain_id %s:chain_version %s', chain_id, chain_version)

        logger.debug('chain_id is %s, chain_version is %s', chain_id, chain_version)
            
    if len(pchains) != 0:
        for chain in pchains:
            logger.info('publish, chain_id is %s, chain_version is %s', chain_id, chain_version)
            publish_server(chain.get_id(), chain.get_version())


def publish_server(chain_id, chain_version):
    """发布链区块链对应的版本, 并且将安装包的部署信息记录下来.

    Arguments:
        chain_id {string} -- chain id
        chain_version {string} -- 区块链版本
    """

    dir = data.package_dir(chain_id, chain_version)
    if not os.path.isdir(dir):
        consoler.error('publish install package for chain %s version %s failed, no package build for the chain.', chain_id, chain_version)
        logger.warn(
            'version of this chain is not exist, chain is %s, version is %s', chain_id, chain_version)
        return
    mm = meta.Meta(chain_id)
    for host in os.listdir(dir):
        cf = config.Config(chain_id)
        if utils.valid_ip(host):
            cfg_json = dir + '/' + host + '/node0/config.json'
            if os.path.isfile(cfg_json):
                consoler.info('config file is %s' %(cfg_json))
                cf.fromJson(cfg_json)
            else:
                consoler.error('invalid config, config is %s', cfg_json)
            node_dir = dir + '/' + host + '/'
            node_number = 0
            for list_dir in os.listdir(node_dir):
                if 'node' in list_dir:
                    node_number = node_number + 1
            rpc_port = cf.get_rpc_port()
            p2p_port = cf.get_p2p_port()
            channel_port = cf.get_channel_port()
            ret = push_package(dir, host, chain_id, chain_version)
            if ret:
                mm.append(meta.MetaNode(chain_version, host, rpc_port, p2p_port, channel_port,node_number))
        else:
            logger.debug('skip, not invalid host_ip ' + dir)
    consoler.info('\t\t publish install package for chain %s version %s end.', chain_id, chain_version)
    # 将部署信息保存
    mm.write_to_file()

def push_package(dir, host, chain_id, version):
    """推送单个安装包到指定服务器
    
    Arguments:
        dir {string} -- 本地安装包目录        
        pkg {string} -- 安装包名称
    
    Returns:
        [bool] -- 成功返回True,失败返回False
    """

    # check if common dir exist.
    if not os.path.exists(dir + '/common'):
        logger.warn('common dir is not exist, dir is %s, host is %s', dir, host)
        return False

    # check if host dir exist.
    if not os.path.exists(dir + '/' + host):
        logger.warn('host dir is not exist, dir is %s, host is %s', dir, host)
        return False

    # create dir on the target server
    ret = ansible.mkdir_module(host, ansible.get_dir() + '/' + chain_id)
    if not ret:
        consoler.error('chain %s host %s, publish install package failed.', chain_id, host)
        return ret
    
    # push common package
    ret = ansible.copy_module(host, dir + '/common/', ansible.get_dir() + '/' + chain_id)
    if not ret:
        consoler.error('chain %s host %s, push common dir failed.', chain_id, host)
        return ret
    
    # push host dir
    ret = ansible.copy_module(host, dir + '/' + host + '/', ansible.get_dir() + '/' + chain_id)
    if not ret:
        consoler.error('chain %s host %s, publish install package failed', chain_id, host)
        return ret
    
    logger.info('push package success, dir is %s, host is %s, chain_id is %s, chain_version is %s', dir, host, chain_id, version)
    
    return True

def push_node(dir, host, chain_id, version, index, force = False):
    # 
    node_dir = Chain(chain_id, version).data_dir() + ('/%s/node%d/' % (host, index))
    # check if nodeIndex dir exist.
    if not os.path.exists(node_dir):
        logger.warn('%s not exist, index is %d, host is %s',node_dir, index, host)
        consoler.error('push node%d failed, node dir not exist.', index)
        return False
    
    # create dir on the target server
    ret = ansible.mkdir_module(host, ansible.get_dir() + '/' + chain_id)
    if not ret:
        consoler.error('push node%d failed, mkdir operation failed.', index)
        return ret
    
    # check if common dir exist.
    if not os.path.exists(dir + '/common'):
        logger.warn('common dir not exist, dir is %s, host is %s', dir, host)
        consoler.error('push node%d failed, common dir not exist.', index)
        return False
    
    # push common package
    ret = ansible.copy_module(host, dir + '/common/', ansible.get_dir() + '/' + chain_id)
    if not ret:
        consoler.error('push node%d failed, push common dir failed.', index)
        return ret
    
    if not force:
        # check if nodeIndex already push
        pass
    
    # push nodeIndex dir
    ret = ansible.copy_module(host, node_dir, ansible.get_dir() + '/' + chain_id)
    if not ret:
        consoler.error('push node%d failed.', index)
        return ret
    
    




    

    





