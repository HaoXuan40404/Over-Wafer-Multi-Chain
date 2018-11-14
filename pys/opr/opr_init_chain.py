# coding:utf-8
import os
import json
import shutil
from pys import path
from pys.tool import utils
from pys.log import logger
from pys.log import consoler
from pys.error.exp import MCError

def init_ansible(hosts_conf, add_opr=False):
    try:
        if not os.path.exists(hosts_conf):
            raise MCError('hosts_conf not exisits! ')
        if add_opr:
            src = '/etc/ansible/hosts'
            dst = '/etc/ansible/hosts.bak'
            if not os.path.exists(src):
                raise MCError('/etc/ansible/hosts not exisits! ')
            os.rename(src, dst)
            f = open(src, 'w')
            f.close()
        for line in open(hosts_conf):
            line = line.strip()
            host_value = line.split()
            print(host_value,type(host_value))
            if len(host_value) != 4:
                raise Exception('hosts_conf type error ,host_line -> %s',host_value)
            user = host_value[0]
            ip = host_value[1]
            port = host_value[2]
            passwd = host_value[3]
            if not utils.valid_string(user):
                raise Exception('user type error ,user -> %s, host_line -> %s'%(user, host_value))
            if not utils.valid_ip(ip):
                raise Exception('ip type error ,ip -> %s, host_line -> %s'%(ip, host_value))
            if not utils.valid_port(int(port)):
                raise Exception('port type error ,port -> %s, host_line -> %s' %(port, host_value))
            if not utils.valid_string(passwd):
                raise Exception('passwd type error ,passwd -> %s, host_line -> %s'%(passwd, host_value))
            (status, result) = utils.getstatusoutput('bash ' + path.get_path() + '/scripts/ansible_init.sh' + ' ' + user + ' ' + ip + ' ' + port + ' ' + passwd)
            if status != 0:
                logger.warn(' ansible_init failed! status is %d, output is %s.', status, result)
                raise MCError('ansible_init failed! status is %d, output is %s.' % (status, result))
            logger.info(' ansible_init success! status is %d, output is %s', status, result)
    except MCError as me:
        consoler.error(' \033[1;31m %s \033[0m', me)
    except Exception as e:
        consoler.error(' \033[1;31m ansible_init failed! excepion is %s.\033[0m', e)
        # logger.error('  ssh_copy_add.sh init failed! Result is %s'%result)
