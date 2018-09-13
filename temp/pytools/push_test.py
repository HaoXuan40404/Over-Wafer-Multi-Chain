#!/usr/bin/python

import os
import commands
import ConfigParser
import ansible

global chain_number
global ip_number
global package_number


class ChainIpPackage:
    '''init class'''
    def __init__(self):
        print("__init__start...")
        self.send_var = ansible.AnsibleBuild()
        # chian_map = set({})
        # for i in range(0,chain_number):
        #     chian_map.add('chain_' + str(i))
        #read ini

    '''get ip'''
    def ip_get(self,PATH):
        cfg_ini = ConfigParser.ConfigParser()
        cfg_ini.read(PATH)
        number = cfg_ini.options('nodes') 
        print(number,type(number))
        mapp = []
        for i in range(0,len(number)):
            mapp.append(cfg_ini.get('nodes',number[i]))
        print(mapp,type(mapp))
        ip = []
        for i in range(0,len(mapp)):
            ip.append(mapp[i].split("  ")[0])
            print(ip,type(ip))
        self.ip = ip
        return 0

    '''push package'''
    def push_package(self,send_PATH):
        for i in range(0,len(self.ip)):
            self.send_var.test_module(self.ip[i],send_PATH)
        return 0


'''main function'''
if __name__=="__main__":
    
    PATH = './config.ini'
    unit_test = ChainIpPackage()
    unit_test.ip_get(PATH)
    unit_test.push_package('./')

    # cfg_ini = ConfigParser.ConfigParser()
    # cfg_ini.read('./config.ini')
    # number = cfg_ini.options('nodes') 
    # print(number,type(number))
    # mapp = []
    # for i in range(0,len(number)):
    #     mapp.append(cfg_ini.get('nodes',number[i]))
    # print(mapp,type(mapp))
    # ip = []
    # for i in range(0,len(mapp)):
    #     ip.append(mapp[i].split("  ")[0])
    #     print(ip,type(ip))

