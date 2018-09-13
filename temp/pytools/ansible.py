#!/usr/bin/python

import os
import commands
import ConfigParser

class AnsibleBuild(object):
    '''init class'''
    def __init__(self):
        print("__init__start...")
    
    '''cpoy module'''
    def copy_module(self,ip,src,dest):
        os.system('bash ./ansible.sh copy ' + ip + ' ' + src + ' ' + dest)
        return 0

    '''unarchive module'''
    def unarchive_module(self,ip,src,dest):
        os.system('bash ./ansible.sh unarchive ' + ip + ' ' + src + ' ' + dest)
        return 0

    '''build module'''
    def build_module(self,ip,PATH):
        os.system('bash ./ansible.sh build ' + ip + ' ' + PATH)
        return 0

    '''start module'''
    def start_module(self,ip,PATH):
        os.system('bash ./ansible.sh start ' + ip + ' ' + PATH)
        return 0

    '''stop module'''
    def stop_module(self,ip,PATH):
        os.system('bash ./ansible.sh stop ' + ip + ' ' + PATH)
        return 0

    '''test module'''
    def test_module(self,ip,PATH):
        os.system('bash ./ansible.sh this ' + ip + ' ' + PATH)
        return 0

    '''check module
    check servers status
    '''
    def check_module(self,ip,PATH):
        return 0

    '''monitor module
    monitor chains status including' 
    'node messenge, blk_number, viewchange, node live or not, node on which server, peers'
    '''
    def monitor_module(self,ip,PATH):
        return 0


'''main function'''
if __name__=="__main__":

    src = 'test words'
    dest = './build/mkdir'
    ip = '10.107.105.137'
    #print("this test string is " + src.replace("\r","") + ' ' + dest.replace("\r",""))
    config = AnsibleBuild()
    config.test_module(ip,src)
    # test_str ='bash ./ansible.sh this ' + src + ' ' + dest
    # print("this string is " + test_str)
    # os.system(test_str)