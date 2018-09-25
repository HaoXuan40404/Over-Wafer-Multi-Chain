import os

from pys import ansible, utils
from pys.chain import data
from pys.chain import meta
from pys.log import logger, consoler


def check_chain_resolve(chain):
    if chain[0] == 'all':
        dir = data.meta_dir_base()
        for chain_id in os.listdir(dir):
            check_environment(chain_id)
    else:
        for i in range(len(chain)):
            chain_get = chain[i].split(':')
            if len(chain_get) == 1:
                if utils.valid_string(chain_get[0]):
                    check_environment(chain_get[0])
                else:
                    consoler.info('chain_resolve error')
                    logger.error('error chain_resolve')
            elif len(chain_get) == 2:
                if utils.valid_string(chain_get[0]):
                    ansible.environment_module(chain_get[1], ansible.get_dir() + '/' + chain_get[0])
                else:
                    consoler.info('chain_resolve error')
                    logger.error('error chain_resolve')

            else:
                consoler.info('chain_resolve error')
                logger.error('error chain_resolve')


def check_environment(chain_id):
    mm = meta.Meta(chain_id)
    logger.info('check_environment action, chain_id is ' + chain_id)
    mm.load_from_file()
    for k,v in mm.get_nodes().items():
        logger.debug('host ip is ' + k)
        ansible.environment_module(k, ansible.get_dir() + '/' + chain_id)


