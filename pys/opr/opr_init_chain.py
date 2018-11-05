# coding:utf-8
import os
import json
import shutil
from pys import path

def init_chain(hosts_conf):
 
    os.system('sudo bash ' + path.get_path() + '/scripts/hostsname.sh' + ' ' + hosts_conf)
    os.system('bash ./scripts/ssh_copy_add.sh')