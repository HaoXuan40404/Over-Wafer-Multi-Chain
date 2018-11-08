#!/usr/bin/python
# coding:utf-8

import argparse
import os
import sys

from pys import path
# init path info first
owmc_dir = os.path.split(os.path.realpath(__file__))[0]
sys.path.append(owmc_dir + '/pys')
path.set_path(owmc_dir)

from pys.conf import mconf
from pys.tool import ca
from pys.tool import ansible
from pys import version
from pys.log import logger
from pys.log import consoler
from pys.opr import opr_check
from pys.opr import opr_tools
from pys.opr import opr_init_chain
from pys.opr import opr_start
from pys.opr import opr_stop
from pys.opr import opr_check
from pys.opr import opr_env_check
from pys.opr import opr_diagnose
from pys.opr import opr_list
from pys.opr import opr_export
from pys.opr import opr_register
from pys.opr import opr_publish
from pys.opr import opr_build
from pys.opr import opr_expand


def init():
    """[init function]
    """

    # init pwd dir
    # owmc_dir = os.getcwd()
    owmc_dir = os.path.split(os.path.realpath(__file__))[0]
    sys.path.append(owmc_dir + '/pys')
    path.set_path(owmc_dir)

    logger.info('main init ,owmc_dir is %s', owmc_dir)

    # parser mchain.conf for project initialize
    mconf.parser(owmc_dir + '/conf/mchain.conf')

    # init agent name
    ca.set_agent(mconf.get_agent())

    # init ca dir
    ca.set_ca_path(owmc_dir + '/data/ca/' + ca.get_agent())

    # init ansible push base dir
    ansible.set_dir(mconf.get_ansible_dir())

def Usage():
    """cmd usage
    """

    parser = argparse.ArgumentParser(
        description=' Build fisco-bcos install pkg for multi chain and manage the chain  package with ansible. ')

    parser.add_argument('--version',
                        action='store_true', help='show OWMC\'s version. ')
    parser.add_argument('--ansibleinit', nargs=1, metavar=(' hosts config file '),
                        help=' initialize ansible configuration file, need sudo permissions. ')
    parser.add_argument('--cainit', action='store_true',
                        help=' initialize cert. ')

    pkg_group = parser.add_argument_group(
        ' Build, Expand, Export, List Chain Package Options ')
    pkg_group.add_argument('--build', nargs=2, metavar=('./config.conf or ./conf/',
                                                        'fisco_path'), help=' build chain packages with the specified configuration file')
    pkg_group.add_argument('--expand', nargs=2, metavar=('./config.conf, dir'),
                           help='build chain packages on exist chain')
    pkg_group.add_argument('--export', nargs=3, metavar=('chain_id', 'chain_version',
                                                         'dest_path'), help='export build package out.')
    pkg_group.add_argument('--pkglist', nargs='+', metavar=('all or chain_id'
                                                            ), help='list build packages info.')
    pkg_group.add_argument('--direct', action='store_true',
                           help='follow --export/-E, package of chain will export without reordering')

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
    mgr_group.add_argument('--force', action='store_true',
                           help='follow --publish, all package of chain will be republished')

    tools_group = parser.add_argument_group(
        ' Other Tools Options ')
    tools_group.add_argument('--telnet', nargs='+', metavar=(
        '\'all\' or host_ip or chain_id'), help='test ansible')
    tools_group.add_argument('--envcheck', nargs='+', metavar=('all or host_ip'),
                             help='check build environment')
    tools_group.add_argument('--docmd', nargs=2, metavar=(' host ip or chain id or \'all\'',
                                                                'shell cmd or shell file, eg ： \'ls -lt\'〝test.sh'), help='execute a shell command or shell file on remote server')
    tools_group.add_argument('--pushfile', nargs=3, metavar=('host ip or chain id or \'all\'',
                                                                   'file or dir to be push.', 'dst dir.'), help='push one file or dir to remote server.')
    tools_group.add_argument('--chainca', nargs=1, metavar=('chain_dir',),
                             help='generate root cert')
    tools_group.add_argument('--agencyca', nargs=3, metavar=('agency_dir',
                                                             'chain_dir', ' agency_name'), help='generate agency cert')
    tools_group.add_argument('--nodeca', nargs=3, metavar=('agency_dir',
                                                           'node _dir', 'node_name'), help='generate node cert')
    tools_group.add_argument('--sdkca', nargs=2, metavar=('sdk_dir',
                                                          'agency_dir'), help='generate sdk cert')
    tools_group.add_argument('--gm', action='store_true',
                             help='follow ----chainca/--agencyca/--agencyca/--sdkca, is gm ca operation.')

    args = parser.parse_args()
    os.path.exists
    if args.version:
        version.version()
    elif args.build:
        consoler.info(' build operation begin.')
        opr_build.build(args.build[0], args.build[1])
        consoler.info(' build operation end.')
    elif args.expand:
        consoler.info(' expand operation begin.')
        opr_expand.expand(args.expand[0], args.expand[1])
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
        opr_publish.publish_chain(chain, args.force)
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
        ca.generate_root_ca(chain_dir, args.gm)
        consoler.info(' chain cert end.')
    elif args.agencyca:
        consoler.info(' agency cert begin.')
        agency_dir = args.agencyca[0]
        chain_dir = args.agencyca[1]
        agency_name = args.agencyca[2]
        ca.generator_agent_ca(agency_dir, chain_dir, agency_name, args.gm)
        consoler.info(' agency cert end.')
    elif args.nodeca:
        consoler.info(' agency cert begin.')
        agency_dir = args.nodeca[0]
        node_dir = args.nodeca[1]
        node_name = args.nodeca[2]
        ca.generator_node_ca(agency_dir, node_dir, node_name, args.gm)
        consoler.info(' agency cert end.')
    elif args.sdkca:
        consoler.info(' sdk cert begin.')
        sdk_dir = args.sdkca[0]
        agency_dir = args.sdkca[1]
        ca.generator_sdk_ca(agency_dir, sdk_dir, args.gm)
        consoler.info(' sdk cert end.')
    elif args.envcheck:
        consoler.info(' envcheck operation begin.')
        hosts = args.envcheck
        opr_env_check.env_check(hosts)
        consoler.info(' envcheck operation end.')
    elif args.telnet:
        consoler.info(' telnet operation begin.')
        telnet_list = args.telnet
        opr_tools.telnet_ansible(telnet_list)
        consoler.info(' telnet operation end.')
    elif args.ansibleinit:
        opr_init_chain.init_chain(args.ansibleinit[0])
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
    elif args.lshost:
        consoler.info(' lshost operation begin.')
        opr_list.ls_host(args.lshost)
        consoler.info(' lshost operation end.')
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
