from pys.chain import data
import os
from pys import ansible
from pys import utils
from pys.log import logger

dest_dir = '/data/' 
class Publish:

    def publish_server(self,chain_id, chain_version):
        dir = data.Data().dir(chain_id,chain_version)
        if not os.path.isdir(dir):
            logger.warn('dir not exist, dir is ' + dir)
            return
        print('dir=,',dir)
        for host in os.listdir(dir):
            print(host,type(host))
            if utils.valid_ip(host):
                print('value ip=>',host)
                ansible.mdir_module(host,dest_dir + chain_id)
                ansible.copy_module(host, dir  + '/' + host  + '/' + '*', dest_dir + chain_id + '/')
            else:
                print("wrong host_ip!",host)
            

# utils.invalid_ip(. . .)

    