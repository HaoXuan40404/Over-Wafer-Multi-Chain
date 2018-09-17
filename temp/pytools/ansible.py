#!/usr/bin/python

import os
import commands
import ConfigParser

class AnsibleBuild(object):

    def __init__(self):
        '''
        init class
        '''
        print("__init__start...")
    
    
    def copy_module(self,ip,src,dest):
        '''
        cpoy module
        '''
        os.system('bash ./ansible.sh copy ' + ip + ' ' + src + ' ' + dest)
        return 0

    
    def unarchive_module(self,ip,src,dest):
        '''
        unarchive module
        '''
        os.system('bash ./ansible.sh unarchive ' + ip + ' ' + src + ' ' + dest)
        return 0

    def mdir_module(self,ip,dest):
        '''
        mkdir module
        '''
        os.system('bash ./ansible.sh shell ' + ip + ' ' + src + ' ' + dest)
        return 0

    
    def build_module(self,ip,PATH):
        '''
        build module
        '''
        os.system('bash ./ansible.sh build ' + ip + ' ' + PATH)
        return 0

    
    def start_module(self,ip,PATH):
        '''
        start module
        '''
        os.system('bash ./ansible.sh start ' + ip + ' ' + PATH)
        return 0

    
    def stop_module(self,ip,PATH):
        '''
        stop module
        '''
        os.system('bash ./ansible.sh stop ' + ip + ' ' + PATH)
        return 0

    
    def test_module(self,ip,PATH):
        '''
        test module
        '''
        os.system('bash ./ansible.sh this ' + ip + ' ' + PATH)
        return 0


    def check_module(self,ip,PATH):
        '''check module
        check servers status
        '''
        return 0


    def monitor_module(self,ip,PATH):
        '''monitor module
            monitor chains status including' 
            node messenge, blk_number, viewchange, node live or not, node on which server, peers'
        '''
        return 0



if __name__=="__main__":
    '''
    main function
    '''

    src = 'test words'
    dest = './build/mkdir'
    ip = '10.107.105.137'
    #print("this test string is " + src.replace("\r","") + ' ' + dest.replace("\r",""))
    config = AnsibleBuild()
    config.test_module(ip,src)
    # test_str ='bash ./ansible.sh this ' + src + ' ' + dest
    # print("this string is " + test_str)
    # os.system(test_str)