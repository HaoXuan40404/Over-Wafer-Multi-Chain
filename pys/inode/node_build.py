import os
import shutil
import logging

# get logger
logger = logging.getLogger("instance")

fisco_bcos_dir=''
genesis_json_dir=''
web3sdk_dir=''
bootstrapnodes_json_dir=''
log_conf_dir=''
scripts_dir=''

def copy_bootstrapnodes_json(dstdir):
    '''
    拷贝bootstrapnodes.json文件到节点数据目录
    '''
    shutil.copy(bootstrapnodes_json_dir + '/bootstrapnodes.json', dstdir)

def copy_fisco_bcos(dstdir):
    '''
    拷贝fisco-bcos二进制文件到安装文件夹
    '''
    shutil.copy(fisco_bcos_dir + '/fisco-bcos', dstdir)

def copy_web3sdk(dstdir):
    '''
    拷贝web3sdk到安装文件夹
    '''
    shutil.copytree(web3sdk_dir + '/web3sdk', dstdir)

def copy_genesis_json(dstdir):
    '''
    拷贝创世块文件genesis.json到节点目录
    '''
    shutil.copy(genesis_json_dir + '/genesis.json', dstdir)

def copy_log_conf(dstdir):
    '''
    拷贝创世块文件genesis.json到节点目录
    '''
    shutil.copy(log_conf_dir + '/log.conf', dstdir)

def copy_scripts(dstdir):
    '''
    拷贝脚本文件到节点的安装文件夹
    '''
    shutil.copy(scripts_dir + '/start.sh', dstdir)
    shutil.copy(scripts_dir + '/stop.sh', dstdir)
    shutil.copy(scripts_dir + '/check.sh', dstdir)
    shutil.copy(scripts_dir + '/register.sh', dstdir)
    shutil.copy(scripts_dir + '/unregister.sh', dstdir)

def copy_node_scripts(dstdir):
    '''
    拷贝节点脚本文件到节点目录
    '''
    shutil.copy(scripts_dir + '/node_start.sh', dstdir + '/start.sh')
    shutil.copy(scripts_dir + '/node_stop.sh', dstdir + '/stop.sh')
    shutil.copy(scripts_dir + '/node_check.sh', dstdir + '/check.sh')

def build_install_dir(dir, count):
    '''
    构建一个节点的安装包目录结构
    '''
    logger.info('build_install_dir ,dir is %s, count is %d', dir, count)

    if os.path.isdir(dir):
        raise Exception('dir aleady exist, dir ', dir)

    if count <= 0:
        raise Exception('count le zero, count ', count)

    os.makedirs(dir)
    copy_scripts(dir)
    copy_web3sdk(dir)

    index = 0
    while index < count:
        node_dir = dir + ('/node%d' % index)
        os.makedirs(node_dir)
        copy_log_conf(node_dir)
        copy_genesis_json(node_dir)
        copy_node_scripts(node_dir)
        index += 1

    logger.info('build_install_dir end.')


