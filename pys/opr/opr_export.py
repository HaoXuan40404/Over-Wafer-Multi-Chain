# coding:utf-8
import os
import shutil
from pys import utils
from pys.chain.chain import Chain
from pys.chain import data
from pys.log import consoler, logger
from pys.opr import opr_tools

def export_package(chain_id, chain_version, dest):
    """export chain_id:chain_version install package
    
    Arguments:
        chain_id {[string]} -- chain id
        chain_version {[string]} -- chain version
        dest {[string]} -- dest
    """

    if utils.valid_chain_id(chain_id):
        chain = Chain(chain_id, chain_version)
        if chain.exist():
            if not os.path.exists(dest):
                os.makedirs(dest)
            dir = chain.data_dir()
            for host in os.listdir(dir):
                if not utils.valid_ip(host):
                    logger.debug('not invalid host_ip ' + host)
                    continue

                utils.getstatusoutput('cp ' + dir + '/' + host + ' ' + dest + '/')
                utils.getstatusoutput('cp ' + dir + '/' + 'common' + '/*' +   ' ' + dest + '/' + host)

                """
                for file_common in os.listdir(dir + '/common'):
                    if os.path.isdir(dir + '/common/' + file_common):
                        shutil.copytree(
                            dir + '/common/' + file_common, dest + '/' + host + '/' + file_common)
                    elif os.path.isfile(dir + '/common/' + file_common):
                        shutil.copy(dir + '/common/' + file_common,
                                    dest + '/' + host + '/')
                                    """
        else:
            consoler.error(
                ' No package build for chain_id(%s):chain_version(%s). ', chain_id, chain_version)
    else:
        consoler.error(' Not invalid chain_id, chain_id is %s', chain_id)
