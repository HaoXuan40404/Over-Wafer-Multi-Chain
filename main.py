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
from pys.opr import opr_check, opr_tools, opr_init_chain, opr_start, opr_stop, opr_check, opr_env_check, opr_diagnose, opr_list, opr_export, opr_register
from pys.chain import build
from pys.chain import expand
from pys.chain import publish


def init():
    """[init function]
    """

    # init pwd dir
    pwd = os.getcwd()
    sys.path.append(pwd + '/pys')
    path.set_path(pwd)

    logger.info('main init ,pwd is %s', pwd)

    # parser mchain.conf for project initialize
    mconf.parser(pwd + '/conf/mchain.conf')

    # init agent name
    ca.set_agent(mconf.get_agent())

    # init ca dir
    ca.set_ca_path(pwd + '/data/ca/' + ca.get_agent())

    # init ansible push base dir
    ansible.set_dir(mconf.get_ansible_dir())

def Usage():
    """cmd usage
    """

    parser = argparse.ArgumentParser(
        description=' Build fisco-bcos install pkg for multi chain and manage the chain installation package builded with ansible. ')

    parser.add_argument('--version',
                        action='store_true', help='show OWMC\'s version. ')
    parser.add_argument('--init', action='store_true',
                        help=' initialize ansible configuration file, need sudo permissions. ')
    
    pkg_group = parser.add_argument_group(' Build, Expand, Export, List Chain Package Options ')
    pkg_group.add_argument('--build', nargs=2, metavar=('./config.conf or ./conf/',
                                                        'fisco_path'), help=' build chain packages with the specified configuration file')
    pkg_group.add_argument('--expand', nargs=2, metavar=('./config.conf, dir'),
                           help='build chain packages on exist chain')
    pkg_group.add_argument('--export', nargs=3, metavar=('chain_id', 'chain_version',
                                                         'dest_path'), help='export build package out.')
    pkg_group.add_argument('--pkglist', nargs='+', metavar=('all or chain_id'
                                                            ), help='list build packages info.')
    pkg_group.add_argument('--direct', action='store_true',
                           help='effect with --export/-E, with this opt, package of chain will export without directory reordering')

    mgr_group = parser.add_argument_group(
        ' Manage Published Chain With Ansible Options ')
    mgr_group.add_argument('--publish', nargs='+', metavar=('chain_id:version'
                                                            ), help='publish packages')
    mgr_group.add_argument('--start', nargs='+', metavar=('all or chain_id or',
                                                          'chain_id:host_ip'), help='start node')
    mgr_group.add_argument('--stop', nargs='+', metavar=('all or chain_id or',
                                                         'chain_id:host_ip'), help='stop node')
    mgr_group.add_argument('--register', nargs=3, metavar=('chain_id ', 'host_ip',
                                                           'node'), help='register node on node with expand opr build')
    mgr_group.add_argument('--unregister', nargs=3, metavar=('chain_id ',  'host_ip',
                                                             'node'), help='unregister node')
    mgr_group.add_argument('--diagnose', nargs='+', metavar=('all or chain_id or',
                                                             'chain_id:host_ip'), help='diagnose node')
    mgr_group.add_argument('--check', nargs='+', metavar=('all or chain_id or',
                                                          'chain_id:host_ip'), help='check servers status')
    mgr_group.add_argument('--publist', nargs='+', metavar=('all or chain_id or'
                                                            ), help='list published packages info.')
    mgr_group.add_argument('--lshost', nargs='+', metavar=('host_ip'),
                           help='ls published packages\' host')
    mgr_group.add_argument('-f', '--force', action='store_true',
                           help='effect with --publish/-p, with this opt, all package of chain will be republished')

    tools_group = parser.add_argument_group(
        ' Other Tools Options ')
    tools_group.add_argument('-t', '--telnet', nargs='+', metavar=(
        '\'all\' or host_ip or chain_id'), help='test ansible')
    tools_group.add_argument('--env_check', nargs='+', metavar=('all or host_ip'),
                        help='check build environment')

    tools_group.add_argument('-d', '--do_cmd', nargs=2, metavar=(' host ip or chain id or \'all\'',
                                                            'shell cmd or shell file, eg ： \'ls -lt\'、test.sh'), help='execute a shell command or shell file on remote server')
    tools_group.add_argument('-P', '--push_file', nargs=3, metavar=('host ip or chain id or \'all\'',
                                                               'file or dir to be push.', 'dst dir.'), help='push one file or dir to remote server.')
    tools_group.add_argument('--chainca', nargs=1, metavar=('chain ca dir to be generate.',),
                        help='generate root cert')
    tools_group.add_argument('--agencyca', nargs=3, metavar=('agency ca dir to be generate.',
                                                        'chain ca dir', ' agency name'), help='generate agency cert')
    tools_group.add_argument('--nodeca', nargs=3, metavar=('agency ca dir',
                                                      'node ca dir to be generate.', 'node_name'), help='generate node cert')
    tools_group.add_argument('--sdkca', nargs=2, metavar=('sdk ca dir',
                                                     'agency ca dir'), help='generate sdk cert')
    args = parser.parse_args()
    if args.version:
        version.version()
    elif args.build:
        consoler.info(' build operation begin.')
        build.chain_build(args.build[0], args.build[1])
        consoler.info(' build operation end.')
    elif args.expand:
        consoler.info(' expand operation begin.')
        expand.chain_expand(args.expand[0], args.expand[1])
        consoler.info(' expand operation end.')
    elif args.check:
        consoler.info(' check operation begin.')
        chain = args.check
        opr_check.check_chain(chain)
        consoler.info(' check operation end.')
    elif args.diagnose:
        consoler.info(' diagnose operation begin.')
        chain = args.diagnose
        opr_diagnose.diagnose_chain(chain)
        consoler.info(' diagnose operation end.')
    elif args.publish:
        consoler.info(' publish operation begin.')
        chain = args.publish
        publish.publish_chain(chain, args.force)
        consoler.info(' publish operation end.')
    elif args.register:
        consoler.info(' register operation begin.')
        opr_register.register(
            args.register[0], args.register[1], args.register[2])
        consoler.info(' register operation end.')
    elif args.unregister:
        consoler.info(' unregister operation begin.')
        opr_register.unregister(
            args.unregister[0], args.unregister[1], args.unregister[2])
        consoler.info(' unregister operation end.')
    elif args.start:
        consoler.info(' start operation begin.')
        chain = args.start
        opr_start.start_chain(chain)
        consoler.info(' start operation end.')
    elif args.stop:
        consoler.info(' stop operation begin.')
        chain = args.stop
        opr_stop.stop_chain(chain)
        consoler.info(' stop operation end.')
    elif args.publist:
        consoler.info(' publist operation begin.')
        chain = args.publist
        opr_list.pub_list(chain)
        consoler.info(' publist operation end.')
    elif args.pkglist:
        consoler.info(' pkglist operation begin.')
        chain = args.pkglist
        opr_list.pkg_list(chain)
        consoler.info(' pkglist operation end.')
    elif args.docmd:
        consoler.info(' docmd operation begin.')
        params = args.docmd
        opr_tools.do_cmd(params[0], params[1])
        consoler.info(' docmd operation end.')
    elif args.pushfile:
        consoler.info(' pushfile operation begin.')
        params = args.pushfile
        opr_tools.push_file(params[0], params[1], params[2])
        consoler.info(' pushfile operation end.')
    elif args.chainca:
        consoler.info(' chain cert begin.')
        chain_dir = args.chainca[0]
        chain_name = args.chainca[1]
        if args.gm:
            ca.gm_generate_root_ca(chain_dir, chain_name)
        else:
            ca.generate_root_ca(chain_dir, chain_name)
        consoler.info(' chain cert end.')
    elif args.agencyca:
        consoler.info(' agency cert begin.')
        agency_dir = args.agencyca[0]
        chain_dir = args.agencyca[1]
        agency_name = args.agencyca[2]
        if args.gm:
            ca.gm_generator_agent_ca(agency_dir, chain_dir, agency_name)
        else:
            ca.generator_agent_ca(agency_dir, chain_dir, agency_name)
        consoler.info(' agency cert end.')
    elif args.nodeca:
        consoler.info(' agency cert begin.')
        agency_dir = args.nodeca[0]
        node_dir = args.nodeca[1]
        node_name = args.nodeca[2]
        if args.gm:
            ca.gm_generator_node_ca(agency_dir, node_dir, node_name)
        else:
            ca.generator_node_ca(agency_dir, node_dir, node_name)
        consoler.info(' agency cert end.')
    elif args.sdkca:
        consoler.info(' sdk cert begin.')
        sdk_dir = args.sdkca[0]
        agency_dir = args.sdkca[1]
        if args.gm:
            ca.gm_generator_sdk_ca(agency_dir, sdk_dir)
        else:
            ca.generator_sdk_ca(agency_dir, sdk_dir)
        consoler.info(' sdk cert end.')
    elif args.env_check:
        consoler.info(' env_check operation begin.')
        hosts = args.env_check
        opr_env_check.env_check(hosts)
        consoler.info(' env_check operation end.')
    elif args.telnet:
        consoler.info(' telnet operation begin.')
        telnet_list = args.telnet
        opr_tools.telnet_ansible(telnet_list)
        consoler.info(' telnet operation end.')
    elif args.init:
        opr_init_chain.init_chain()
        consoler.info(' ansible init success.')
    elif args.cainit:
        consoler.info(' cert init begin.')
        ca.init_ca(args.cainit[0])
        consoler.info(' cert init end.')
    elif args.export:
        consoler.info(' export operation begin.')
        opr_export.export_package(
            args.export[0], args.export[1], args.export[2], args.direct)
        consoler.info(' export operation end.')
    elif args.ls_host:
        consoler.info(' ls_host operation begin.')
        opr_list.ls_host(args.ls_host)
        consoler.info(' ls_host operation end.')
    else:
        consoler.error(
            '\033[1;31m invalid operation,  \"python main.py -h\" can be used to show detailed usage. \033[0m')
    return 0

def main():
    try:
        init()
    except Exception as e:
        consoler.error(' \033[1;31m OWMC init fault , %s \033[0m', e)
    else:
        Usage()


if __name__ == '__main__':
    main()
