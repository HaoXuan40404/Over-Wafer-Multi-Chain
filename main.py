# coding:utf-8

import argparse
import os
import sys

from pys import mconf
from pys import ca
from pys import ansible
from pys import path
from pys import version
from pys.log import logger
from pys.log import consoler
from pys.chain import opr
from pys.chain import build
from pys.chain import publish
from pys.checktools import check_environment 



def init():
    # 获取当前目录, 用来初始化各个模块的依赖路径
    pwd = os.getcwd()
    sys.path.append(pwd + '/pys')
    path.set_path(pwd)

    logger.info('main init ,pwd is %s', pwd)

    # 解析mchain.conf配置
    mconf.parser(pwd + '/conf/mchain.conf')

    # 初始化证书(机构名称、证书路径)
    ca.set_agent(mconf.get_agent())
    ca.set_ca_path(pwd + '/data/ca')

    # ansible远程推送的根目录
    ansible.set_dir(mconf.get_ansible_dir())

def cmd_view():
    parser = argparse.ArgumentParser(
        description='Description of multi-chain usage.')
    parser.add_argument('--version', action='store_true',
                        help='version of multi-chain')
    parser.add_argument('--build', nargs=2, metavar=('./config.conf or ./conf/',
                                                     'fisco_path'), help='Output => package. Build all package under directory ./data/chain/ according to the input.')
    parser.add_argument('--list', nargs='+', metavar=('all or chain_id or',
                                                      'chain_id_1 chain_id_2'), help='Output =>  list all pkg info.')
    parser.add_argument('--publish', nargs='+', metavar=('chain_id:version eg.',
                                                         'chain_id_1:version_1 chain_id_2:version_1 chain_id_3:version_2.etc.'), help='Output => publish all package to servers')
    parser.add_argument('--check', nargs='+', metavar=('all or chain_id or',
                                                       'chain_id:host_ip'), help='Output => check servers status')
    parser.add_argument('--stop', nargs='+', metavar=('all or chain_id or',
                                                      'chain_id:host_ip'), help='Output => stop node')
    parser.add_argument('--start', nargs='+', metavar=('all or chain_id or',
                                                       'chain_id:host_ip'), help='Output => start node')
    parser.add_argument('--monitor', nargs='+', metavar=('all or chain_id or',
                                                         'chain_id:host_ip'), help='Output => monitor node')
    parser.add_argument('--envircheck', nargs='+', metavar=('all or chain_id or',
                                                            'chain_id:host_ip'), help='Output => check build environment of server of the chain.')
    parser.add_argument('--chainca', nargs=1, metavar=('./dir_chain_ca(SET)',), 
                                                        help='Output => the cert of chain that set on the SET directory')
    parser.add_argument('--agencyca', nargs=3, metavar=('./dir_agency_ca(SET)',
                                                      './chain_ca_dir', 'The Agency Name'), help='Output => the cert of agency that set on the SET directory')
    parser.add_argument('--sdkca', nargs=2, metavar=('./dir_sdk_ca(SET)',
                                                      './dir_agency_ca'), help='Output => the cert of sdk for agency that set on the SET directory')
    parser.add_argument('--echo', nargs='+', metavar=('all or host_ip or',
                                                      'host_ip1 host_ip2'), help='Output => test ansible of servers is useful or not')
    args = parser.parse_args()
    if args.version:
        version.version()
    elif args.build:
        consoler.info(' build opr begin.')
        build.chain_build(args.build[0], args.build[1])
        consoler.info(' build opr end.')
    elif args.check:
        consoler.info(' check opr begin.')
        chain = args.check
        opr.check_chain_resolve(chain)
        consoler.info(' check opr end.')
    elif args.publish:
        consoler.info(' publish opr begin.')
        chain = args.publish
        publish.publish_chain(chain)
        consoler.info(' publish opr end.')
    elif args.start:
        consoler.info(' start opr begin.')
        chain = args.start
        opr.start_chain_resolve(chain)
        consoler.info(' start opr end.')
    elif args.stop:
        consoler.info(' stop opr begin.')
        chain = args.stop
        opr.stop_chain_resolve(chain)
        consoler.info(' stop opr end.')
    elif args.monitor:
        consoler.info(' monitor opr begin.')
        chain = args.monitor
        opr.monitor_chain_resolve(chain)
        consoler.info(' monitor opr end.')
    elif args.list:
        consoler.info(' list opr begin.')
        chain = args.list
        opr.list_chain_resolve(chain)
        consoler.info(' list opr end.')

    elif args.chainca:
        consoler.info(' chain cert begin.')
        chain_dir = args.chainca[0]
        ca.generate_root_ca(chain_dir)
        consoler.info(' chain cert end.')
    elif args.agencyca:
        consoler.info(' agency cert begin.')
        agency_dir = args.agencyca[0]
        chain_dir = args.agencyca[1]
        agency_name = args.agencyca[2]
        ca.generator_agent_ca(agency_dir, chain_dir, agency_name)
        consoler.info(' agency cert end.')
    elif args.sdkca:
        consoler.info(' sdk cert begin.')
        sdk_dir = args.sdkca[0]
        agency_dir = args.sdkca[1]
        ca.generator_sdk_ca(agency_dir)
        os.system('mv ' + agency_dir + '/sdk ' + sdk_dir + '/sdk')

        consoler.info(' sdk cert end.')

    # elif args.envircheck:
    #    chain = args.envircheck
    #    check_environment.check_chain_resolve(chain)
    elif args.echo:
        consoler.info(' echo opr begin.')
        echo_list = args.echo
        opr.echo_ansible(echo_list)
        consoler.info(' echo opr end.')
    else:
        consoler.info('\t [ERROR] invalid opr,  \"python main.py -h\" can be used to show detailed usage.')
    return 0


def main():
    init()
    cmd_view()


if __name__ == '__main__':
    main()
