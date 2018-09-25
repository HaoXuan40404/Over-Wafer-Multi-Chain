#coding:utf-8

import re
from pys.log import logger
from pys.log import consoler

def valid_ip(ip):
    p = re.compile('^((25[0-5]|2[0-4]\d|[01]?\d\d?)\.){3}(25[0-5]|2[0-4]\d|[01]?\d\d?)$')
    if p.match(ip):
        return True
    else:
        return False

def valid_port(port):
    if isinstance(port, int) and (port > 0) and (port <= 65535):
        return True
    else:
        return False

def valid_string(s):
    if (isinstance(s, str) or isinstance(s, unicode)) and (len(s) > 0):
        return True
    else:
        return False

def replace(filepath, old, new):
    '''
    '''
    with open(filepath, 'r+') as f:
        all_lines = f.readlines()
        f.seek(0)  
        f.truncate() 
        for line in all_lines:
            line = line.replace(old, new)
            f.write(line)

def valid_chain_id(chain_id):
    try: 
        int(chain_id)
        return True
    except Exception as e: 
        consoler.error('%s is not a valid chain_id', e)
        logger.error('%s is not a valid chain_id', e)
        return False
