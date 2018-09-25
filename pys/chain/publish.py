# coding:utf-8
import os
from pys import utils
from pys import ansible
from pys.log import logger
from pys.log import consoler
from pys.chain import meta
from pys.chain import data
from pys.chain.chain import Chain


def publish_chain(chains):
    """发布命令行传入的所有指定版本的区块链.
    
    Arguments:
        list_chain_version {list} -- 需要发布的链, 格式为chain_id:chain_version, 可以一次发布多个, 多个之间使用空格分离.
    
    Returns:
        无返回
    """
    chains = []
    for i in range(len(chains)):
        chain = chains[i].split(':')
        if len(chain) != 2:
            logger.error('not chain_id:chain_version format, str is %s', chains[i])
            consoler.info('\t [ERROR] skip, invalid publish format, chain_id:chain_version should require, chain is %s', chain)
            continue

        chain_id = chain[0]
        chain_version = chain[1]
        chains.append(Chain(chain_id, chain_version))
        consoler.info('\t append publish chain, chain_id %s:chain_version %s', chain_id, chain_version)
        logger.debug('chain_id is %s, chain_version is %s', chain_id, chain_version)
            
    if len(chains) != 0:
        for chain in chains:
            publish_server(chain.get_id(), chain.get_version())

    logger.info('chain_version is %s', chain_version)


def publish_server(chain_id, chain_version):
    """发布链区块链对应的版本, 并且将安装包的部署信息记录下来.

    Arguments:
        chain_id {string} -- 区块链id
        chain_version {string} -- 区块链版本
    """

    dir = data.package_dir(chain_id, chain_version)
    if not os.path.isdir(dir):
        consoler.info('\t\t [ERROR] publish install package for chain %s version %s failed, data dir not exist', chain_id, chain_version)
        logger.warn(
            'version of this chain is not exist, chain is %s, version is %s', chain_id, chain_version)
        return
    mm = meta.Meta(chain_id)
    for host in os.listdir(dir):
        if utils.valid_ip(host):
            # 后续要添加这里的推送是否成功的判断
            ansible.mkdir_module(host, ansible.get_dir() + '/' + chain_id)
            ansible.copy_module(host, dir + '/' + host + '/',
                                ansible.get_dir() + '/' + chain_id)
            mm.append(meta.MetaNode(chain_version, host, 0, 0, 0))
        else:
            logger.debug('skip, not invalid host_ip ' + dir)
    # 将部署信息保存
    mm.write_to_file()
