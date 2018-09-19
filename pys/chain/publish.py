import os
#coding:utf-8
from pys import utils
from pys import ansible
from pys.chain import data
from pys.log import logger
from pys.chain import meta

def publish_chain(list_chain_version):
    
    list_chain = list_chain_version.split(' ')

    if isinstance(list_chain_version,str):
        
        for i in range(0, len(list_chain)):
            chainaddversion = list_chain[i].split(':')
            chain_id = chainaddversion[0]
            chain_version = chainaddversion[1]
            try:
                logger.debug('chain_version is %s', chain_version)
                publish_server(chain_id, chain_version)
            except Exception as e:
                print('chain_version %s failed, skip ...', e)
                logger.warn('parser chain_version %s end exception, e %s ', chain_version,  e)

    else:
        
        print('unkown chain_version path , chain_version is %s ', chain_version)
        logger.warn('unkown chain_version path , chain_version is %s', chain_version)
    
    logger.info('chain_version is %s', chain_version)

   
    return 0


def publish_server(chain_id, chain_version):
    dir = data.package_dir(chain_id,chain_version)
    if not os.path.isdir(dir):
        logger.warn('dir not exist, dir is ' + dir)
        return
    mm = meta.Meta(chain_id)
    for host in os.listdir(dir):
        if utils.valid_ip(host):
            ansible.mkdir_module(host, ansible.get_dir() + '/' + chain_id)
            ansible.copy_module(host, dir  + '/' + host  + '/', ansible.get_dir() + '/' + chain_id)
            mm.append(meta.MetaNode(chain_version, host, 0, 0, 0))
        else:
            logger.debug('skip, not invalid host_ip ' + dir)
    mm.write_to_file()
