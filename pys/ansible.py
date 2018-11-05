# coding:utf-8
import os
import re

from pys import utils
from pys import path
from pys.log import logger
from pys.log import consoler


class Ansible:
    """Ansible configuration, to configure the target folder for push, default = '/data'
    """

    dir = '/data'

    def __repr__(self):
        return '[dir] %s' % (Ansible.dir)


def set_dir(dir):
    Ansible.dir = dir


def get_dir():
    return Ansible.dir


def mkdir_module(ip, dest):
    """[Using ansible.sh mkdir_module create dictionary ]
    
    Arguments:
        ip {string} -- corresponding server host ip
        dest {string} -- dir path
    
    Returns:
        int -- success return True, else return False.
    """

    (status, result) = utils.getstatusoutput('bash ' + path.get_path() +
                                                '/scripts/ansible.sh mkdir ' + ip + ' ' + dest)
    logger.debug('mkdir action , status %s, output %s' % (status, result))
   
    if status:
        consoler.warn(' ansible mkdir failed, host is %s, dst is %s, status is %s, output is %s.', ip, dest, status, result)
        logger.warn('mkdir action failed, status %s, result %s ' % (status, result))
    elif not (result.find('SUCCESS') + 1):
        consoler.warn(' ansible mkdir failed, host is %s, dst is %s, status is %s, output is %s.', ip, dest, status, result)
        logger.warn('mkdir action failed, output %s' % (result))
    else:
        return True
    return False


def copy_module(ip, src, dest):
    """[Using ansible.sh copy_module, push package to servers]
    
    Arguments:
        ip {string} -- corresponding server host ip
        src {string} -- files which push
        dest {string} -- corresponding server dir path

    Returns:
        bool -- true or false.
    """

    (status, result) = utils.getstatusoutput('bash ' + path.get_path() +
                                                '/scripts/ansible.sh copy ' + ip + ' ' + src + ' ' + dest)
    logger.debug('copy action , status %s, output %s' % (status, result))
   
    if status:
        logger.warn('copy action failed, status %s' % (status))
        consoler.warn(' ansible copy failed, host is %s, src is %s, dst is %s, status is %s, output is %s.', ip, src, dest, status, result)
    elif not (result.find('SUCCESS') + 1):
        consoler.warn(' ansible copy failed, host is %s, src is %s, dst is %s, status is %s, output is %s.', ip, src, dest, status, result)
        logger.warn('copy action failed, output %s' % (result))
    else:
        consoler.info(' ansible copy success, host is %s, src is %s, dst is %s.', ip, src, dest)
        return True
    return False


def unarchive_module(ip, src, dest):
    """[Using ansible.sh unarchive_module, compress files to the corresponding server and extract it]
    
    Arguments:
        ip {[string]} -- [corresponding server host ip]
        src {[string]} -- [files dir path]
        dest {[string]} -- [corresponding server dir path]
    
    Returns:
        [bool] -- [true or false]
    """


    (status, result) = utils.getstatusoutput('bash ' + path.get_path() +
                                                '/scripts/ansible.sh unarchive ' + ip + ' ' + src + ' ' + dest)
    logger.debug('unarchive action , status %s, output %s' % (status, result))
   
    if status:
        logger.warn('unarchive action failed, status %s' % (status))
        consoler.warn(' ansible unarchive  failed, host is %s, src is %s, dst is %s, status is %s, output is %s.', ip, src, dest, status, result)
    elif not (result.find('SUCCESS') + 1):
        logger.warn('unarchive action failed, output %s' % (result))
        consoler.warn(' ansible unarchive failed, host is %s, src is %s, dst is %s, status is %s, output is %s.', ip, src, dest, status, result)
    else:
        consoler.info(' ansible unarchive success, host is %s, src is %s, dst is %s.', ip, src, dest)
        return True
    return False

def start_module(ip, dest):
    """Using ansible.sh start_module, start nodes
    
    Arguments:
        ip {string} -- corresponding server host ip
        dest {string} -- corresponding server dir path
    
    Returns:
        bool -- true or false
    """

    (status, result) = utils.getstatusoutput('bash ' + path.get_path() +
                                                '/scripts/ansible.sh start ' + ip + ' ' + dest)
    logger.debug('start action , status %s, output %s' % (status, result))
    
    if status:
        logger.warn('start action failed, status %s' % (status))
        consoler.warn(' ansible start  failed, host is %s, dst is %s, status is %s, output is %s.', ip, dest, status, result)
    elif not (result.find('SUCCESS') + 1):
        logger.warn('start action failed, output %s' % (result))
        consoler.warn(' ansible start failed, host is %s, dst is %s, status is %s, output is %s.', ip, dest, status, result)
    else:
        consoler.info(' ansible start success, host is %s, output is %s.', ip, result)
        return True
    return False

def register_module(ip, dest, index):
    """Using ansible.sh register_module, start nodes
    
    Arguments:
        ip {string} -- corresponding server host ip
        dest {string} -- corresponding server dir path
        index {int} -- node index to be register
    
    Returns:
        bool -- true or false
    """

    (status, result) = utils.getstatusoutput('bash ' + path.get_path() +
                                                '/scripts/ansible.sh register ' + ip + ' ' + dest + ' ' + str(index))
    logger.debug(' register action, status %s, output %s' % (status, result))
    
    if status:
        consoler.warn(' ansible register  failed, host is %s, index is %s, dst is %s, status is %s, output is %s.', ip, str(index), dest, status, result)
    elif not (result.find('SUCCESS') + 1):
        consoler.warn(' ansible register failed, host is %s, index is %s, dst is %s, status is %s, output is %s.', ip, str(index), dest, status, result)
    elif not (result.find('sucess') + 1):
        consoler.warn(' ansible register failed, host is %s, index is %s, dst is %s, status is %s, output is %s.', ip, str(index), dest, status, result)
    else:
        consoler.info(' ansible register success, host is %s, index is %s, output is %s.', ip, str(index), result)
        return True
    return False

def unregister_module(ip, dest, index):
    """Using ansible.sh unregister_module, start nodes
    
    Arguments:
        ip {string} -- corresponding server host ip
        dest {string} -- corresponding server dir path
        index {int} -- node index to be register
    
    Returns:
        bool -- true or false
    """

    (status, result) = utils.getstatusoutput('bash ' + path.get_path() +
                                                '/scripts/ansible.sh unregister ' + ip + ' ' + dest + ' ' + str(index))
    logger.debug(' unregister action, status %s, output %s' % (status, result))
    
    if status:
        consoler.warn(' ansible unregister  failed, host is %s, index is %s, dst is %s, status is %s, output is %s.', ip, str(index), dest, status, result)
    elif not (result.find('SUCCESS') + 1):
        consoler.warn(' ansible unregister failed, host is %s, index is %s, dst is %s, status is %s, output is %s.', ip, str(index), dest, status, result)
    elif not (result.find('sucess') + 1):
        consoler.warn(' ansible register failed, host is %s, index is %s, dst is %s, status is %s, output is %s.', ip, str(index), dest, status, result)
    else:
        consoler.info(' ansible unregister success, host is %s, index is %s, output is %s.', ip, str(index), result)
        return True
    return False

def stop_module(ip, dest):
    """Using ansible.sh stop_module, stop nodes
    
    Arguments:
        ip {string} -- corresponding server host ip
        dest {string} -- corresponding server dir path
    
    Returns:
        bool -- true or false
    """

    (status, result) = utils.getstatusoutput('bash ' + path.get_path() +
                                                '/scripts/ansible.sh stop ' + ip + ' ' + dest)
    logger.debug('stop action , status %s, output %s' % (status, result))

    if status:
        logger.warn('stop action failed, status %s' % (status))
        consoler.warn(' ansible stop failed, host is %s, dst is %s, status is %s, output is %s.', ip, dest, status, result)
    elif not (result.find('SUCCESS') + 1):
        logger.warn('stop action failed, output %s' % (result))
        consoler.warn(' ansible stop failed, host is %s, dst is %s, status is %s, output is %s.', ip, dest, status, result)
    else:
        consoler.info(' ansible stop success, host is %s, output is %s.', ip, result)
        return True
    return False



def check_module(ip, dest):
    """Using ansible.sh check_module, check chain status
    
    Arguments:
        ip {string} -- corresponding server host ip
        dest {string} -- corresponding server dir path
    
    Returns:
        bool -- true or false
    """

    (status, result) = utils.getstatusoutput('bash ' + path.get_path() +
                                                '/scripts/ansible.sh check ' + ip + ' ' + dest)
    logger.debug('check action , status %s, output %s' % (status, result))
    
    if status:
        logger.warn('check action failed, status %s' % (status))
        consoler.warn(' ansible check failed, host is %s, dst is %s, status is %s, output is %s.', ip, dest, status, result)
    elif not (result.find('SUCCESS') + 1):
        logger.warn('check action failed, output %s' % (result))
        consoler.warn(' ansible check failed, host is %s, dst is %s, status is %s, output is %s.', ip, dest, status, result)
    else:
        consoler.info(' ansible check success, host is %s, output is %s.', ip, result)
        return True
    
    return False




def telnet_module(ip, msg='HelloWorld!'):
    """using ansible.sh telnet module, echo 'HelloWorld' to screen to check ansible is useful.

    Arguments:
        ip {string} -- host ip

    Keyword Arguments:
        msg {string} -- test string (default: {'HelloWorld!'})

    Returns:
        [bool] -- ansible useful echo return True, else False.
    """

    (status, result) = utils.getstatusoutput('bash ' + path.get_path() +
                                                '/scripts/ansible.sh telnet ' + ip + ' ' + msg)
    logger.debug('telnet action , status %s, output %s' % (status, result))
    if status:
        consoler.error(' \033[1;31m  ansible telnet failed, host is %s, output is %s \033[0m', ip, result)
    elif not (result.find('SUCCESS') + 1):
        consoler.error(' \033[1;31m  ansible telnet failed, host is %s, output is %s \033[0m', ip, result)
    else:
        consoler.info(' ansible telnet success, host is %s, output is %s', ip, result)
        return True
    return False



def cmd_module(ip, cmd):
    """Using ansible.sh cmd_module, execute commands on the corresponding server.

    Arguments:
        ip {string} -- server host ip

    Keyword Arguments:
        msg {string} -- execute commands

    Returns:
        [bool] -- true or false
    """
    cmd = '"' + cmd + '"'
    
    (status, result) = utils.getstatusoutput('bash ' + path.get_path() +
                                                '/scripts/ansible.sh cmd ' + ip + ' ' + cmd)
    logger.debug(' cmd action , status %s, output %s' % (status, result))
    if status:
        consoler.error(' \033[1;31m  ansible cmd failed, host is %s, output is %s \033[0m', ip, result)
    elif not (result.find('SUCCESS') + 1):
        consoler.error(' \033[1;31m  ansible cmd failed, host is %s, output is %s \033[0m', ip, result)
    else:
        consoler.info(' ansible cmd success, host is %s, cmd is %s.', ip, cmd)
        return True
    return False


def diagnose_module(ip, dest):
    """Using ansible.sh diagnose_module, call script -> monotor.sh, Check status of nodes
    Arguments:
        ip {string} -- corresponding server host ip
        dest {string} -- corresponding server dir path
    """

    (status, result) = utils.getstatusoutput('bash ' + path.get_path() +
                                                '/scripts/ansible.sh diagnose ' + ip + ' ' + dest)
    logger.debug('diagnose action , status %s, output %s' % (status, result))
    if status:
        consoler.error(' \033[1;31m  ansible diagnose failed, host is %s, output is %s \033[0m', ip, result)
    elif not (result.find('SUCCESS') + 1):
        consoler.error(' \033[1;31m  ansible diagnose failed, host is %s, output is %s \033[0m', ip, result)
    else:
        consoler.info(' ansible diagnose success, host is %s, result is %s.', ip, result)
        return True
    return False


def env_check(ip, src):
    """Check whether the environment of the corresponding server satisfy the fisco bcos running conditions.
    
    Keyword Arguments:
        ip {string} -- [corresponding server host ip] (default: {'all'})
    """

    os.system('bash ' + path.get_path() +
                                                '/scripts/ansible.sh env_check ' + ip + ' ' + src)
    #(status, result) = commands.getstatusoutput('bash ' + path.get_path() +
    #                                            '/scripts/ansible.sh env_check ' + ip + ' ' + src)

    # logger.debug('env_check action , status %s, output %s' % (status, result))
    # if status:
    #     consoler.error(' ansible env_check failed, host is %s, output is %s', ip, result)
    # elif not (result.find('SUCCESS') + 1):
    #     consoler.error(' ansible env_check failed, host is %s, output is %s', ip, result)
    # else:
    #     consoler.info(' ansible env_check success, host is %s, output is \n%s', ip, result)
    #     return True
    # return False