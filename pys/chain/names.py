
import os
import sys
import json
import time
import shutil
from pys.chain import data
from pys.log import logger
from pys.exp import MCError


class Names:
    def __init__(self):
        self.names = {}
        self.load()

    def clear(self):
        self.names = {}

    def get_name(self, chain_id):
        name = str(chain_id)
        if chain_id in self.names:
            name = self.names[chain_id]
        logger.debug(' get name chain id is %s, chain name is %s.', chain_id, name)
        return name

    def append(self, chain_id, name):
        if chain_id in self.names:
            return False
        logger.debug(
            ' append one name  chain id is %s, chain name is %s', chain_id, name)
        self.names[chain_id] = name
        return True

    def to_json(self):
        return json.dumps(self, default=lambda obj: obj.__dict__, indent=4)

    def write(self):
        if not os.path.exists(data.package_names_dir()):
            data.create_names_dir()

        names_file = data.package_names_dir() + '/names.json'
        names_bak_file = names_file + '_bak_' + \
            time.strftime("%Y-%m-%d_%H-%M%S", time.localtime())
        if os.path.exists(names_file):
            shutil.copy(names_file, names_bak_file)
            logger.info(
                'names.json is exist, backup it, name is ' + names_bak_file)
        try:
            with open(names_file, "w+") as f:
                f.write(self.to_json())
                logger.info(
                    ' write info names.json, content is ' + self.to_json())
        except Exception as e:
            logger.error(
                ' write names.json failed, exception is %s', e)
            # raise or not ???
            # raise MCError(' write names.json failed, exception is %s' % e)

    def load(self):

        self.clear()
        namesjson = data.package_names_dir() + '/names.json'
        if not os.path.exists(namesjson):
            logger.info(' names.json is not exist, path is %s', namesjson)
            return

        logger.debug(' load begin, path is %s', namesjson)

        try:
            with open(namesjson) as f:
                jsondata = json.load(f)
                if 'names' in jsondata:
                    for k in jsondata['names'].keys():
                        chain_id = k
                        chain_name = jsondata['names'][chain_id]
                        self.append(chain_id, chain_name)
                        logger.debug(
                            ' load one name, chain id is %s, chain name is %s', chain_id, chain_name)
                return True
        except Exception as e:
                logger.error(
                    ' parser namesjson failed, namesjson is %s, exception is %s', namesjson, e)
                return False

        logger.info(' load names end, info %s', self.names)
