# coding:utf-8
from pys.tool import ansible, utils
from pys.log import consoler, logger
from pys import path

def env_check(hosts):
    """[check and confirm the environment normally]
    
    Arguments:
        hosts {string} -- host list
    """
    if hosts[0] == 'all':
        ansible.env_check('all', path.get_path())
    else:
        for host in hosts:
            if utils.valid_ip(host):
                ansible.env_check(host, path.get_path())
            else:
                consoler.log(' skip, not invalid host, host is %s', host)