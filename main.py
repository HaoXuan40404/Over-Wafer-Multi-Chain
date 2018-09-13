#coding:utf-8

import sys
import os
import logging

from pys import log
from pys import ca
from pys import version
from pys import data
from pys import build

def init():
    # 获取当前目录, 用来初始化各个模块的依赖路径 
    pwd = os.getcwd()
    # logging初始化
    log.init_logging(pwd + '/conf/logging.conf')
    # 初始化证书(机构名称、证书路径)
    ca.set_agent('WB')
    ca.set_ca_path(pwd + '/data/ca')
    # 初始化数据目录
    data.set_data_dir(pwd + '/data/chain')
    # version
    version.set_release_note_path(pwd + '/release_note.txt')

def version():
    version.version('./release_note.txt')
    sys.exit(-1)

def main():
    init()





=======
    parser = argparse.ArgumentParser('multi-chain usage')
    parser.add_argument('--config', type=str, dest='config',
                        help="input config file which in ini format")
    parser.add_argument("-V", "--version", action="store_true",
                        help="version of multi-chain")
    args = parser.parse_args()
>>>>>>> .theirs
    print(args)
    for arg in args.__dict__:
        if arg == 'version' and args.version:
            version()
        elif arg == 'config' and args.config is not None:
            config_file = args.config
            print(config_file)

<<<<<<< .mine

=======

>>>>>>> .theirs
if __name__ == '__main__':
    main()
