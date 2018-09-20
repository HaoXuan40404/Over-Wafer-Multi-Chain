# coding:utf-8

import argparse
import os
import sys

from pys import ca
from pys import ansible
from pys import path
from pys import version
from pys.log import logger
from pys.chain import opr
from pys.chain import build
from pys.chain import publish
from pys.checktools import check_environment 
from pys.checktools import readchain



def init():
    # 获取当前目录, 用来初始化各个模块的依赖路径
    pwd = os.getcwd()
    sys.path.append(pwd + '/pys')
    path.set_path(pwd)

    # 初始化证书(机构名称、证书路径)
    ca.set_agent('WB')
    ca.set_ca_path(pwd + '/data/ca')


def cmd_view():
    parser = argparse.ArgumentParser(
        description='Description of multi-chain usage.')
    parser.add_argument('--version', action='store_true',
                        help='version of multi-chain')
    parser.add_argument('--build', nargs=2, metavar=('./config.conf or ./conf/',
                                                     'fisco_path'), help='build all package by config.')
    parser.add_argument('--list', nargs='+', metavar=('all or chain_id or',
                                                      'chain_id_1 chain_id_2'), help='list all pkg info.')
    parser.add_argument('--publish', nargs='+', metavar=('chain_id:version eg.',
                                                         'chain_id_1:version_1 chain_id_2:version_1 chain_id_3:version_2.etc.'), help='publish all package')
    parser.add_argument('--check', nargs='+', metavar=('all or chain_id or',
                                                       'chain_id:host_ip'), help='check servers status')
    parser.add_argument('--stop', nargs='+', metavar=('all or chain_id or',
                                                      'chain_id:host_ip'), help='stop all node')
    parser.add_argument('--start', nargs='+', metavar=('all or chain_id or',
                                                       'chain_id:host_ip'), help='start all node')
    parser.add_argument('--monitor', nargs='+', metavar=('all or chain_id or',
                                                         'chain_id:host_ip'), help='monitor all node')
    parser.add_argument('--envircheck', nargs='+', metavar=('all or chain_id or',
                                                            'chain_id:host_ip'), help='check build environment of all server of the chain.')
    parser.add_argument('--echo', nargs='+', metavar=('all or host_ip or',
                                                      'host_ip1 host_ip2'), help='test servers ansible useful or not')
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
    elif args.list:
        chain = args.list
        opr.list_chain_resolve(chain)
    elif args.envircheck:
        chain = args.envircheck
        check_environment.check_chain_resolve(chain)
    elif args.echo:
        echo_list = args.echo
        opr.echo_ansible(echo_list)
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
