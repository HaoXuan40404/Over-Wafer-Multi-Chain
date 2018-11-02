# coding:utf-8
import os
import shutil
from pys import utils
from pys.chain.chain import Chain
from pys.chain import data
from pys.log import consoler, logger
from pys.opr import opr_tools

def export_package(chain_id, chain_version, dest, direct):
    """export chain_id:chain_version install package
    
    Arguments:
        chain_id {[string]} -- chain id
        chain_version {[string]} -- chain version
        dest {[string]} -- dest
        direct {[string]}
    """

    logger.debug(' chain id is %s, chain version is %s, dest dir is %s, is direct is %s', chain_id, chain_version, dest, direct)

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

                if direct:
                    utils.getstatusoutput('cp -r ' + dir  + '/*'  + ' ' + dest)
                else:
                    utils.getstatusoutput('cp -r ' + dir + '/' + host + ' ' + dest + '/')
                    utils.getstatusoutput('cp -r ' + dir + '/' + 'common' + '/*' +   ' ' + dest + '/' + host)

                consoler.info(' Export chain_id(%s) chain_version(%s) success.', chain_id, chain_version)
        else:
            consoler.error(
                '\033[1;31m No package build for chain_id(%s):chain_version(%s). \033[0m', chain_id, chain_version)
    else:
        consoler.error(' \033[1;31m Not invalid chain_id, chain_id is %s \033[0m', chain_id)
