# coding:utf-8
import os
import json
import shutil
from pys import path
from pys import ansible, utils
from pys.chain.meta import *
from pys.chain.package import AllChain
from pys.chain.package import ChainVers
from pys.chain.package import VerHosts
from pys.chain.package import HostNodeDirs
from pys.chain.port import AllChainPort
from pys.log import logger
from pys.log import consoler
from pys.chain import data
from pys.chain import package

def init_chain(hosts_conf):
 
    os.system('sudo bash ./scripts/hostsname.sh' + ' ' + hosts_conf)
    os.system('bash ./scripts/ssh_copy_add.sh')