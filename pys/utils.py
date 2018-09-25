#coding:utf-8

import re
from pys.log import logger
from pys.log import consoler

def valid_chain_id(chain_id):
    """[判断chain id是否有效]
    
    Arguments:
        ip {[string]} -- [chain id]
    
    Returns:
        [bool] -- [如果为是有效chain id返回true，否则返回false]
    """

    try: 
        int(chain_id)
        return True
    except Exception as e: 
        consoler.error('%s is not a valid chain_id', e)
        logger.error('%s is not a valid chain_id', e)
        return False

def valid_ip(ip):
    """[判断IP是否有效]
    
    Arguments:
        ip {[string]} -- [ip号]
    
    Returns:
        [bool] -- [如果为有效ip返回true，否则返回false]
    """

    p = re.compile('^((25[0-5]|2[0-4]\d|[01]?\d\d?)\.){3}(25[0-5]|2[0-4]\d|[01]?\d\d?)$')
    if p.match(ip):
        return True
    else:
        return False

def valid_port(port):
    """[判断端口号port是否有效]
    
    Arguments:
        ip {[string]} -- [port端口号]
    
    Returns:
        [bool] -- [如果为端口号有效返回true，否则返回false]
    """

    if isinstance(port, int) and (port > 0) and (port <= 65535):
        return True
    else:
        return False

def valid_string(s):
    """[判断字符串是否有效]
    
    Arguments:
        ip {[string]} -- [字符串]
    
    Returns:
        [bool] -- [如果为是有效字符串返回true，否则返回false]
    """
    
    if (isinstance(s, str) or isinstance(s, unicode)) and (len(s) > 0):
        return True
    else:
        return False

def replace(filepath, old, new):
    """[替换文件中的字符串]
    
    Arguments:
        filepath {[path]} -- [需要替换的文件路径]
        old {[string]} -- [需要替换的字符串]
        new {[string]} -- [替换后的字符串]
    """

    with open(filepath, 'r+') as f:
        all_lines = f.readlines()
        f.seek(0)  
        f.truncate() 
        for line in all_lines:
            line = line.replace(old, new)
            f.write(line)


