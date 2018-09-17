#coding:utf-8

import argparse
import os
import sys

from pys import ca, path, version
# from pys.chain import build
from pys.chain import opr, publish, build


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
    parser.add_argument('--check', nargs = 2, metavar = ('chainID','version'), help='check servers status')
    parser.add_argument('--build', nargs =1 ,metavar = ('./config.conf'), help='build all package')
    parser.add_argument('--publish', nargs = 2, metavar = ('chainID','version'), help='publish all package')
    parser.add_argument('--start', nargs = 2, metavar = ('chainID','version'), help='start all node')
    parser.add_argument('--stop', nargs = 2, metavar = ('chainID','version'), help='stop all node')
    args = parser.parse_args()
    if args.version:
        print("this is version")
        version.version()
    elif args.build:
        print("this is build")
        build.chain_build(args.build[0])
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
    return 0

def main():
    init()
    cmd_view()
    #publish.publish_server('chain_1','v1')
    # build.chain_build(path.get_path() + '/conf/config.conf')
    #命令行 build publish start stop version_print

if __name__ == '__main__':

    main()
