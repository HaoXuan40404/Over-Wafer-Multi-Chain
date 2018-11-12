#coding:utf-8

import os
import shutil
import time

from pys.tool import utils
from pys import path
from pys.log import logger
from pys.log import consoler
from pys.build.config.config import Config
from pys.error.exp import MCError
from pys.build.tool import temp_web3_conf


class Temp:
    def __init__(self, chain, fisco, port):
        self.chain = chain
        self.fisco = fisco
        self.port = port
        logger.info(
            ' build temp node, chain is %s, fisco is %s, port is %s .', chain, fisco, port)
        # build temp node dir.
        self.build()
        # start temp node.
        self.start()
        # sleep for check if start success.
        time.sleep(10)
        # check if temp node start.
        self.is_running()
        logger.info(' temp node constructor end. ')

    def dir(self):
        return self.chain.data_dir() + '/temp'

    def start_shell_file(self):
        file = self.dir() + "/node/start.sh"
        # self.file_check(start_shell_file)
        return file

    def check_shell_file(self):
        file = self.dir() + "/node/check.sh"
        # self.file_check(file)
        return file

    def stop_shell_file(self):
        file = self.dir() + "/node/stop.sh"
        # self.file_check(file)
        return file

    def register_shell_file(self):
        file = self.dir() + "/web3sdk/bin/web3sdk"
        # self.file_check(file)
        return file

    def export_shell_file(self):
        file = self.dir() + "/node/export.sh"
        # self.file_check(file)
        return file

    def build(self):
        logger.info(' build temp dir, dir is %s', self.dir())
        try:
            os.makedirs(self.dir())
            shutil.copytree(path.get_path() + '/tpl/web3sdk',
                            self.dir() + '/web3sdk')

            if self.is_gm():
                shutil.move(self.dir() + '/web3sdk/conf/applicationContext_GM.xml',
                            self.dir() + '/web3sdk/conf/applicationContext.xml')

                shutil.copytree(path.get_path() +
                                '/tpl/GM_temp_node', self.dir() + '/node')

                shutil.copy(self.dir() + '/node/data/sdk/ca.crt',
                            self.dir() + '/web3sdk/conf')
                shutil.copy(self.dir() + '/node/data/sdk/client.keystore',
                            self.dir() + '/web3sdk/conf')
            else:
                shutil.move(self.dir() + '/web3sdk/conf/applicationContext_NB.xml',
                            self.dir() + '/web3sdk/conf/applicationContext.xml')

                shutil.copytree(path.get_path() + '/tpl/temp_node',
                                self.dir() + '/node')

                shutil.copy(self.dir() + '/node/sdk/ca.crt',
                            self.dir() + '/web3sdk/conf')
                shutil.copy(self.dir() + '/node/sdk/client.keystore',
                            self.dir() + '/web3sdk/conf')

            # copy fisco-bcos
            shutil.copy(self.fisco.get_fisco_path(), self.dir() + '/node/')
            # config.json for temp node
            Config('12345', self.port.get_rpc_port(),
                   self.port.get_p2p_port(), self.port.get_channel_port(), True).writeFile(self.dir() + '/node/config.json')

            # web3sdk config for temp node
            utils.replace(self.dir() + '/web3sdk/conf/applicationContext.xml', 'WEB3SDK_NODES_LIST',
                          '<value>node0@127.0.0.1:%s</value>' % str(self.port.get_channel_port()))

        except Exception as e:
            logger.error(
                ' temp node build opr failed , chain is %s, exception is %s .', self.chain, e)
            raise MCError(
                ' build temp node failed, chain is %s, exception is %s ' % (self.chain, e))

    def start(self):
        # check if port temp node will use aleady used by others.
        self.port_check()
        # start temp node.
        start_command = 'bash ' + self.start_shell_file()
        status, output = utils.getstatusoutput(start_command)
        if status != 0:
            raise MCError(
                ' temp node start not success, output is %s ' % output)
        logger.info(' start status, status is %d, output is %s',
                    status, output)

    def stop(self):
        stop_command = 'bash ' + self.stop_shell_file()
        if not os.path.exists(self.stop_shell_file()):
            logger.debug('stop file not exist, file is %s. ', stop_command)
            return
        status, output = utils.getstatusoutput(stop_command)
        logger.debug('stop status, status is %d, output is %s', status, output)

    def register(self, node_json):
        register_command = 'bash %s NodeAction registerNode file:%s' % (
            self.register_shell_file(), node_json)
        # node_all_command = 'bash %s NodeAction all'
        status, output = utils.getstatusoutput(register_command)
        if status != 0:
            logger.error(
                ' register node failed, node_json is %s,status is %d, output is %s', node_json, status, output)
            raise MCError(' register opr failed, status is %d ' % status)

        # node_all_command = 'bash %s NodeAction all'
        # status, output = utils.getstatusoutput(node_all_command)
        # if status != 0:
        #    logger.error(' node action all failed, status is %d, output is %s ', status, output)
        #    raise MCError(' node action all failed, output is %s ' % output)

    def export(self):
        export_command = 'bash ' + self.export_shell_file() + ' ' + self.chain.data_dir() + '/genesis.json'
        status, output = utils.getstatusoutput(export_command)
        if not os.path.exists(self.dir() + '/../genesis.json'):
            logger.error('export genesis.json failed, output is %s', output)
            raise MCError(
                ' export genesis.json failed, output is %s.' % output)
        else:
            logger.debug(
                'export status, status is %d, output is %s', status, output)

    def clean(self):
        self.stop()
        if os.path.exists(self.dir()):
            shutil.rmtree(self.dir())

    def file_check(self, file):
        if not os.path.exists(file):
            raise MCError(' temp node file not exist, file is %s ' % file)

    def port_check(self):
        # rpc port check
        if utils.port_in_use(self.port.get_rpc_port()):
            raise MCError(' temp node rpc port(%s) is in use.' %
                          self.port.get_rpc_port())

        # p2p port check
        if utils.port_in_use(self.port.get_p2p_port()):
            raise MCError(' temp node p2p port(%s) is in use.' %
                          self.port.get_p2p_port())

        # channel port
        if utils.port_in_use(self.port.get_channel_port()):
            raise MCError(' temp node channel port(%s) is in use.' %
                          self.port.get_channel_port())

    def is_running(self):
        check_command = 'bash ' + self.check_shell_file()
        status, output = utils.getstatusoutput(check_command)
        logger.info('check status, status is %d, output is %s', status, output)

        if (output.find('is running') == -1):
            raise MCError(' temp node is not running, outpus is %s' % output)

    def is_gm(self):
        return self.fisco.is_gm()
