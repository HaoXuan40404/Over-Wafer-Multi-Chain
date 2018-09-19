#coding:utf-8

import argparse
import os
import sys

from pys import ansible
from pys import ca, path, version
from pys.chain import build, opr, publish
<<<<<<< HEAD
from pys.log import logger
from pys.checktools import check_environment, readchain
=======
from pys.checktools import check_environment, readchain

>>>>>>> 0f634a1a0102382713c8547e9bc68598218afea3

def init():
    # 获取当前目录, 用来初始化各个模块的依赖路径 
    pwd = os.getcwd()
    sys.path.append(pwd + '/pys')
    path.set_path(pwd)

    # 初始化证书(机构名称、证书路径)
    ca.set_agent('WB')
    ca.set_ca_path(pwd + '/data/ca')

def cmd_view():
    parser = argparse.ArgumentParser(description='multi-chain usage')
    parser.add_argument('--version', action="store_true", help='version of multi-chain')
    parser.add_argument('--check', nargs = 1, metavar = ('chainID'), help='check servers status')
    parser.add_argument('--build', nargs =2 ,metavar = ('./config.conf', 'fisco_path'), help='build all package')
    parser.add_argument('--publish', nargs = 2, metavar = ('chainID','version'), help='publish all package')
<<<<<<< HEAD
    parser.add_argument('--start', nargs = 1, metavar = ('chainID'), help='start all node')
    parser.add_argument('--stop', nargs = 1, metavar = ('chainID'), help='stop all node')
    parser.add_argument('--monitor', nargs = 1, metavar = ('chainID'), help='monitor all node')
    parser.add_argument('--envircheck', nargs = 1, metavar = ('chainID'), help='check build environment of all node')
=======
    parser.add_argument('--start', nargs = 2, metavar = ('chainID','version'), help='start all node')
    parser.add_argument('--stop', nargs = 2, metavar = ('chainID','version'), help='stop all node')
    parser.add_argument('--monitor', nargs = 2, metavar = ('chainID','version'), help='monitor all node')
    parser.add_argument('--envircheck', nargs = 2, metavar = ('chainID','version'), help='check build environment of all node')
>>>>>>> 0f634a1a0102382713c8547e9bc68598218afea3
    args = parser.parse_args()
    if args.version:
        version.version()
    elif args.build:
        build.chain_build(args.build[0], args.build[1])
    elif args.check:
        chain_id = args.check[0]
        opr.check_server(chain_id)
    elif args.publish:
        chain_id = args.publish[0]
        chain_version = args.publish[1]
        publish.publish_server(chain_id, chain_version)
    elif args.start:
        chain_id = args.start[0]
        opr.start_server(chain_id)
    elif args.stop:
        chain_id = args.stop[0]
<<<<<<< HEAD
        opr.stop_server(chain_id)
    elif args.monitor:
        chain_id = args.monitor[0]
        opr.monitor_server(chain_id)
    elif args.envircheck:
        chain_id = args.envircheck[0]
        check_environment.check_environment(chain_id)
=======
        chain_version = args.stop[1]
        opr.stop_server(chain_id, chain_version)
    elif args.monitor:
        chain_id = args.monitor[0]
        chain_version = args.monitor[1]
        opr.monitor_server(chain_id, chain_version)
    elif args.envircheck:
        chain_id = args.envircheck[0]
        chain_version = args.envircheck[1]
        check_environment.check_environment(chain_id, chain_version)
>>>>>>> 0f634a1a0102382713c8547e9bc68598218afea3
    else:
        logger.error('unkown action.')
    return 0

def main():
    init()
    
    cmd_view()
    readchain.mchain_conf('./conf/mchain.conf')
    path = readchain.get_dir()
    ansible.set_dir(path)
<<<<<<< HEAD
#test
=======



>>>>>>> 0f634a1a0102382713c8547e9bc68598218afea3
if __name__ == '__main__':
    main()
