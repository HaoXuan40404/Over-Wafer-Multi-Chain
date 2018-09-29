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


def init():
    """[init函数]
    """

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
    """[执行命令行对应操作]
    """

    parser = argparse.ArgumentParser(
        description='Description of multi-chain usage.')
    parser.add_argument('--version', action='store_true',
                        help='version of multi-chain')
    parser.add_argument('--init_ansible', action='store_true', help='Output => Init ansible hosts need sudo.')                   
    parser.add_argument('--build', nargs=2, metavar=('./config.conf or ./conf/',
                                                     'fisco_path'), help='Output => package. Build all package under directory ./data/chain/ according to the input.')
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
    parser.add_argument('--pkg_list', nargs='+', metavar=('all or chain_id or',
                                                          'chain_id_1 chain_id_2'), help='Output =>  list all build package info.')
    parser.add_argument('--pub_list', nargs='+', metavar=('all or chain_id or',
                                                          'chain_id_1 chain_id_2'), help='Output =>  list all publish info.')
    parser.add_argument('--telnet', nargs='+', metavar=('all or host_ip or',
                                                        'host_ip1 host_ip2'), help='Output => test ansible of servers is useful or not')
    parser.add_argument('--env_check', nargs='+', metavar=('all or host_ip'),
                        help='Output => check build environment of server of the chain.')
    parser.add_argument('--cmd_push', nargs='+', metavar=('all:"cmd_1 cmd_2" or chain_id:"cmd_1 cmd_2" or',
                                                          'hostip:"cmd_1 cmd_2" or "chain:"./test.sh""'), help='Output =>  execute commands to Input.')
    parser.add_argument('--file_push', nargs='+', metavar=('all:scr_path:dest_path or chain_id:scr_path:dest_path or',
                                                          'chain_id:scr_path:dest_path or host_ip:scr_path:dest_path'), help='Output =>  push a file to Input.')
    parser.add_argument('--chainca', nargs=1, metavar=('./dir_chain_ca(SET)',),
                        help='Output => the cert of chain that set on the SET directory')
    parser.add_argument('--agencyca', nargs=3, metavar=('./dir_agency_ca(SET)',
                                                        './chain_ca_dir', 'The Agency Name'), help='Output => the cert of agency that set on the SET directory')
    parser.add_argument('--sdkca', nargs=2, metavar=('./dir_sdk_ca(SET)',
                                                     './dir_agency_ca'), help='Output => the cert of sdk for agency that set on the SET directory')
    args = parser.parse_args()
    if args.version:
        version.version()
    elif args.build:
        consoler.info(' build operation begin.')
        build.chain_build(args.build[0], args.build[1])
        consoler.info(' build operation end.')
    elif args.check:
        consoler.info(' check operation begin.')
        chain = args.check
        opr.check_chain(chain)
        consoler.info(' check operation end.')
    elif args.publish:
        consoler.info(' publish operation begin.')
        chain = args.publish
        publish.publish_chain(chain)
        consoler.info(' publish operation end.')
    elif args.start:
        consoler.info(' start operation begin.')
        chain = args.start
        opr.start_chain(chain)
        consoler.info(' start operation end.')
    elif args.stop:
        consoler.info(' stop operation begin.')
        chain = args.stop
        opr.stop_chain(chain)
        consoler.info(' stop operation end.')
    elif args.monitor:
        consoler.info(' monitor operation begin.')
        chain = args.monitor
        opr.monitor_chain(chain)
        consoler.info(' monitor operation end.')
    elif args.pub_list:
        consoler.info(' pub_list operation begin.')
        chain = args.pub_list
        opr.pub_list(chain)
        consoler.info(' pub_list operation end.')
    elif args.pkg_list:
        consoler.info(' pkg_list operation begin.')
        chain = args.pkg_list
        opr.pkg_list(chain, True)
        consoler.info(' pkg_list operation end.')
    elif args.cmd_push:
        consoler.info(' cmd_push operation begin.')
        chain = args.cmd_push
        opr.cmd_push(chain)
        consoler.info(' cmd_push operation end.')
    elif args.file_push:
        consoler.info(' file_push operation begin.')
        chain = args.file_push
        opr.file_push(chain)
        consoler.info(' file_push operation end.')
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

    elif args.env_check:
        consoler.info(' env_check operation begin.')
        hosts = args.env_check
        opr.env_check(hosts)
        consoler.info(' env_check operation end.')
    elif args.telnet:
        consoler.info(' telnet operation begin.')
        telnet_list = args.telnet
        opr.telnet_ansible(telnet_list)
        consoler.info(' telnet operation end.')
    elif args.init_ansible:
        # 解析hosts.conf配置
        os.system('sudo bash ./scripts/hostsname.sh')
        os.system('sudo bash ./scripts/ssh_copy_add.sh')
        consoler.info(' ansible init success.')
    else:
        consoler.error(
            'invalid operation,  \"python main.py -h\" can be used to show detailed usage.')
    return 0

def main():
    init()
    cmd_view()



if __name__ == '__main__':
    main()
