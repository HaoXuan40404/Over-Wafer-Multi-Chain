#!/usr/bin/python

import os
import time
import argparse





'''help function'''
def help(self):
    return 0



'''main function'''
if __name__=="__main__":
    print('main')
    parser = argparse.ArgumentParser(description='multi-chain usage')
    parser.add_argument('-c', '--config', type=str, dest='config', help='input config file which in ini format')
    parser.add_argument('-v', '--version', action='store_true', help='version of multi-chain')
    parser.add_argument('--new_account', help='generate a new account')
    parser.add_argument('-check', '--CHECK', dest='check',choices=['server_id_1', 'server_id_2', 'server_id_3','all'], help='check servers status'
    'uptime, top, netstat, lsof, ps -ef | grep fisco, du -sh *') #uptime cpu network etc.. use ansible
    #parser.add_argument('-m', '--monitor', action='append', dest='monitor', default=[], help='monitor nodes status') # show a path and read ini to monitor node #choice is a list
    parser.add_argument('-m', '--monitor', dest='monitor', choices=['chain_id_1', 'chain_id_2', 'chain_id_3','all'], help='monitor chains status including' 
    'node messenge, blk_number, viewchange, node live or not, node on which server, peers') #can be exchanged by str_changed 
    # node messenge, blk_number, viewchange, node live or not,
    args = parser.parse_args()

    print(type(args.__dict__))
    if args.__dict__['config']:
        print("config.json")
    elif args.__dict__['version']:
        print("version")
    elif args.__dict__['new_account']:
        print('generate a new account')
    elif args.monitor == '127.0.0.1':
        print("right")
        # else:
        #     print("help")
    print(type(args.__dict__['monitor']))
    print(args.__dict__['monitor'])
    print(args.__dict__['monitor'][0])
    # print(type(args))
    # print(args)
    

    

