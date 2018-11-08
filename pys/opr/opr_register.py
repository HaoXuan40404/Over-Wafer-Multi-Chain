from pys.data_mgr.meta import Meta
from pys.log import consoler, logger
from pys.error.exp import MCError
from pys.tool import ansible


def register(chain_id, host, node):

    logger.debug(' chain_id is %s, host is %s, node is %s',
                 chain_id, host, node)
    meta = Meta(chain_id)
    if not meta.exist():
        consoler.error(' \033[1;31m register failed, chain not published, chain id is %s \033[0m', chain_id)
        return

    try:
        meta.get_host_node(host, node)
    except MCError as me:
        consoler.error(' \033[1;31m register failed, %s  \033[0m', me)
    else:
        ret = ansible.register_module(host, ansible.get_dir() + '/' + chain_id, int(node[4:]))
        if ret:
            consoler.info(' register success, chain_id is %s, host is %s, node is %s. \033[0m', chain_id, host, node)
        else:
            consoler.error(' \033[1;31m register failed, chain_id is %s, host is %s, node is %s. \033[0m', chain_id, host, node)


def unregister(chain_id, host, node):

    logger.debug(' chain_id is %s, host is %s, node is %s',
                 chain_id, host, node)
    meta = Meta(chain_id)
    if not meta.exist():
        consoler.error(' \033[1;31m unregister failed, chain not published, chain id is %s. \033[0m', chain_id)
        return

    try:
        meta.get_host_node(host, node)
    except MCError as me:
        consoler.error(' \033[1;31m unregister failed, %s  \033[0m', me)
    else:
        ret = ansible.unregister_module(host, ansible.get_dir() + '/' + chain_id, int(node[4:]))
        if ret:
            consoler.info(' unregister success, chain_id is %s, host is %s, node is %s.', chain_id, host, node)
        else:
            consoler.error(' \033[1;31m unregister failed, chain_id is %s, host is %s, node is %s. \033[0m', chain_id, host, node)
    
