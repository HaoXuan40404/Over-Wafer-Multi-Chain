#!/usr/bin/python

import os
import time
import argparse
from pys.chain import publish
from pys.chain import opr






def help(self):
    '''publishpublishppublish
    help function
    '''
    return 0




if __name__=="__main__":
    '''
    main function
    '''
    print('main')
    parser = argparse.ArgumentParser(description='multi-chain usage')
    parser.add_argument('-c', '--config', action="store_true", help='input config file which in ini format')
    parser.add_argument('-v', '--version', action="store_true", help='version of multi-chain')
    parser.add_argument('-k', '--check', nargs = 2, help='check servers status')
    parser.add_argument('-g', '--generate', action="store_true", help='generate all package')
    parser.add_argument('-p', '--publish', nargs = 2, help='publish all package')
    parser.add_argument('-s', '--start', nargs = 2, help='start all node')
    parser.add_argument('-t', '--stop', nargs = 2, help='stop all node')
    args = parser.parse_args()
    print(args.check,type(args.check))
    if args.config:
        print("this is config")
    elif args.version:
        print("this is version")
    elif args.check:
        print("this is check")
        chain_id = args.check[0]
        chain_version = args.check[1]
        opr.check_server(chain_id, chain_version)
    elif args.publish:
        print("this is push")
        chain_id = args.publish[0]
        chain_version = args.publish[1]
        publish.publish_server(chain_id, chain_version)
    elif args.start:
        print("this is start")
        chain_id = args.start[0]
        chain_version = args.start[1]
        opr.start_server(chain_id, chain_version)
    elif args.stop:
        print("this is stop")
        chain_id = args.stop[0]
        chain_version = args.stop[1]
        opr.stop_server(chain_id, chain_version)
    else:
        print('error')




    # parser.add_argument('-check', '--CHECK', dest='check',choices=['server_id_1', 'server_id_2', 'server_id_3','all'], help='check servers status'
    # 'uptime, top, netstat, lsof, ps -ef | grep fisco, du -sh *') #uptime cpu network etc.. use ansible
    # parser.add_argument('-m', '--monitor', dest='monitor', choices=['chain_id_1', 'chain_id_2', 'chain_id_3','all'], help='monitor chains status including' 
    # 'node messenge, blk_number, viewchange, node live or not, node on which server, peers') #node messenge, blk_number, viewchange, node live or not,
    # print(type(args.__dict__))
    # if args.__dict__['config']:
    #     print("config.json")
    # elif args.__dict__['version']:
    #     print("version")
    # elif args.__dict__['new_account']:
    #     print('generate a new account')
    # elif args.monitor == '127.0.0.1':
    #     print("right")
    #     # else:
    #     #     print("help")

    # print(type(args))
    # print(args)
    

    

