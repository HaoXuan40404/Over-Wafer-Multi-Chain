#coding:utf-8

import argparse
import os
import sys

from pys import ansible, ca, path, version
from pys.chain import build, opr, publish
from pys.checktools import check_environment, readchain
from pys.log import logger


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
    parser.add_argument('--version', action='store_true', help='version of multi-chain')
    parser.add_argument('--check', nargs = '+', metavar = ('all or chainID or', 'chainID:hostIP'), help='check servers status')
    parser.add_argument('--build', nargs =2 ,metavar = ('./config.conf', 'fisco_path'), help='build all package')
    parser.add_argument('--publish', nargs = '+', metavar = ('chainID:version eg.','chainID_1:version_1 chainID_2:version_1 chainID_3:version_2.etc.'), help='publish all package')
    parser.add_argument('--start', nargs = '+', metavar = ('all or chainID or', 'chainID:hostIP'), help='start all node')
    parser.add_argument('--stop', nargs = '+', metavar = ('all or chainID or', 'chainID:hostIP'), help='stop all node')
    parser.add_argument('--monitor', nargs = '+', metavar = ('all or chainID or', 'chainID:hostIP'), help='monitor all node')
    parser.add_argument('--envircheck', nargs = '+', metavar = ('all or chainID or', 'chainID:hostIP'), help='check build environment of all node')
    parser.add_argument('--test', nargs = '+', metavar = ('all or hostIP or', 'hostIP1 hostIP2'), help='test servers ansible useful or not')
    args = parser.parse_args()
    if args.version:
        version.version()
    elif args.build:
        build.chain_build(args.build[0], args.build[1])
    elif args.check:
        chain = args.check
        opr.check_chain_resolve(chain)
    elif args.publish:
        chain = args.publish
        publish.publish_chain(chain)
    elif args.start:
        chain = args.start
        opr.start_chain_resolve(chain)
    elif args.stop:
        chain = args.stop
        opr.stop_chain_resolve(chain)
    elif args.monitor:
        chain = args.monitor
        opr.monitor_chain_resolve(chain)
    elif args.envircheck:
        chain = args.envircheck
        check_environment.check_chain_resolve(chain)
    elif args.test:
        test_list = args.test
        opr.test_ansible(test_list)
    else:
        logger.error('unkown action.')
    return 0

def main():
    init()
    readchain.mchain_conf('./conf/mchain.conf')
    path = readchain.get_dir()
    ansible.set_dir(path) 
    cmd_view()


if __name__ == '__main__':
    main()
