# coding:utf-8
import os
from pys import utils
from pys import ansible
from pys.log import logger
from pys.chain import meta
from pys.chain import data


def publish_chain(list_chain_version):
    """发布命令行传入的所有指定版本的区块链.
    
    Arguments:
        list_chain_version {list} -- 需要发布的链, 格式为chain_id:chain_version
    
    Returns:
        无返回
    """

    list_chain = list_chain_version

    if isinstance(list_chain_version, list):

        for i in range(0, len(list_chain)):
            temp_list = list_chain[i].split(':')
            if len(temp_list) != 2:
                logger.error('not chain_id:chain_version format, str is %s', list_chain[i])
                continue
            try:
                chain_id = temp_list[0]
                chain_version = temp_list[1]
                logger.debug('chain_id is %s, chain_version is %s', chain_id, chain_version)
                publish_server(chain_id, chain_version)
            except Exception as e:
                print('chain_version %s failed, skip ...' % e)
                logger.warn(
                    'parser chain_version %s end exception, e %s ', chain_version,  e)

    else:

        print('unkown chain_version path , chain_version is %s ' % chain_version)
        logger.warn(
            'unkown chain_version path , chain_version is %s' % chain_version)

    logger.info('chain_version is %s', chain_version)

    return 0


def publish_server(chain_id, chain_version):
    """发布链区块链对应的版本, 并且将安装包的部署信息记录下来.

    Arguments:
        chain_id {string} -- 区块链id
        chain_version {string} -- 区块链版本
    """

    dir = data.package_dir(chain_id, chain_version)
    if not os.path.isdir(dir):
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
