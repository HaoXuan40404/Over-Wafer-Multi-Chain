from pys.chain.meta import Meta
from pys.log import consoler, logger
from pys.exp import MCError
from pys import ansible


def register(chain_id, host, node):

    logger.debug(' chain_id is %s, host is %s, node is %s',
                 chain_id, host, node)
    meta = Meta(chain_id)
    if meta.exist():
        consoler.error(' register failed, chain not published, chain id is %s', chain_id)
        return

    try:
        meta.get_host_node(host, node)
    except MCError as me:
        consoler.error(' register failed, %s ', me)
    else:
        ret = ansible.register_module(host, ansible.get_dir() + '/' + chain_id, int(node[4:]))
        if ret:
            consoler.info(' register success, chain_id is %s, host is %s, node is %s.')
        else:
            consoler.error(' register failed, chain_id is %s, host is %s, node is %s.')


def unregister(chain_id, host, node):

    logger.debug(' chain_id is %s, host is %s, node is %s',
                 chain_id, host, node)
    meta = Meta(chain_id)
    if meta.exist():
        consoler.error(' unregister failed, chain not published, chain id is %s.', chain_id)
        return

    try:
        meta.get_host_node(host, node)
    except MCError as me:
        consoler.error(' unregister failed, %s ', me)
    else:
        ret = ansible.unregister_module(host, ansible.get_dir() + '/' + chain_id, int(node[4:]))
        if ret:
            consoler.info(' unregister success, chain_id is %s, host is %s, node is %s.')
        else:
            consoler.error(' unregister failed, chain_id is %s, host is %s, node is %s.')
    
