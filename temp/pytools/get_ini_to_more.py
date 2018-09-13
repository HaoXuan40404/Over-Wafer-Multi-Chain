#!/usr/bin/python

import os
import time
import ConfigParser

class EnvironmentVariables(object):
    '''init class''' 
    def __init__(self,PATH):
        self.PATH = PATH
        #self.chain_number, self.chain_list, self.p2p_port, self.rpc_port, self.channel_port, self.keystore_pwd, self.clientcert_pwd
        self.chain_list = []

    '''get function'''
    def get_ini(self):
        cfg_ini = ConfigParser.ConfigParser()
        config_file_path=self.PATH
        cfg_ini.read(config_file_path)
        self.chain_number = cfg_ini.getint("common", "chain_number")
        for i in range(1,self.chain_number):
            chainid = "chain_id_" + str(i)
            self.chain_list.append(cfg_ini.get("chain",str(chainid)))
        self.p2p_port = cfg_ini.getint("ports", "p2p_port")
        self.rpc_port = cfg_ini.getint("ports", "rpc_port")
        self.channel_port = cfg_ini.getint("ports", "channel_port")
        self.keystore_pwd = cfg_ini.getint("web3sdk", "keystore_pwd") 
        self.clientcert_pwd = cfg_ini.getint("web3sdk", "clientcert_pwd")

        return 0

    '''print function'''
    def print_ini(self):
        print('chain_number => %d' %(self.chain_number))
        print("chain => %s"  %(type(self.chain_list)))
        print("chain => %s"  %(self.chain_list))
        print("p2p_port => %d" %(self.p2p_port))
        print("rpc_port => %d"  %(self.rpc_port))
        print("channel_port => %d"  %(self.channel_port))
        print("keystore_pwd => %d"  %(self.keystore_pwd))
        print("clientcert_pwd => %d"  %(self.clientcert_pwd))
        return 0
        
    '''return function'''
    def get_chain_number(self):
        return self.chain_number
    


'''main function'''
if __name__=="__main__":
    print('main')
    number = '1232312312'
    for i in range(0,len(number)):
        config_ini = 'config.ini' + str(i)
        test = EnvironmentVariables(config_ini)
        test.get_ini()
        test.print_ini()



