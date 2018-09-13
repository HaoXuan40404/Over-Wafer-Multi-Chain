#!/usr/bin/python

import os
import commands
import sys
sys.path.append('./pytools')
import VarReplace
import time
import ConfigParser


class TempNode(object):
    
    def __init__(self):
        '''init class'''
        global DEFAULT_SYSTEM_CONTRACT_ADDRESS
        DEFAULT_SYSTEM_CONTRACT_ADDRESS="0x919868496524eedc26dbb81915fa1547a20f8998"
        global NODE_ID
        NODE_ID = "8c0fbe3a9b31775fc9786d7ae791e72b299d71bec18f18eb908caf637c71eaab4c691e738c41bc03478dd262077230056a4b0f07e9043445ea5632560326b8f5"
        self.config=VarReplace.VarReplace()

    def config_json(self,config_path,rpc_port,p2p_port,channel_port,chain_id):
        '''build config.json'''
        config_path = config_path
        os.environ['config_path'] = config_path
        os.system('cp ./build/tpl_dir/config.json.tpl ${config_path}')
        # nodes = cfg_ini.get("nodes", "node0")
        #  = nodes.split()
        self.config.get_to_write(config_path,"systemproxyaddress",DEFAULT_SYSTEM_CONTRACT_ADDRESS)
        self.config.get_to_write(config_path,"listenip","127.0.0.1")
        self.config.get_to_write(config_path,"cryptomod","0")
        self.config.get_to_write(config_path,"rpcport",str(rpc_port))
        self.config.get_to_write(config_path,"p2pport",str(p2p_port))
        self.config.get_to_write(config_path,"channelPort",str(channel_port))
        self.config.get_to_write(config_path,"wallet","./build/node0/keys.info")
        self.config.get_to_write(config_path,"keystoredir","./build/node0/keystore")
        self.config.get_to_write(config_path,"datadir","./build/node0/data")
        self.config.get_to_write(config_path,"networkid",str(chain_id))
        self.config.get_to_write(config_path,"logconf","./log.conf")
        return 0

    def application_Context_replace(self,applicationContext_path,clientcert_pwd,keystore_pwd,channel_port,DEFAULT_SYSTEM_CONTRACT_ADDRESS):
        '''build applicationContext.xml'''
        applicationContext_path = applicationContext_path
        os.environ['applicationContext_path'] = applicationContext_path
        os.system('cp ./build/tpl_dir/applicationContext.xml.tpl ${applicationContext_path}')
        self.config.replace_str(applicationContext_path,'${CLIENTCERT_PWD}',str(clientcert_pwd))
        self.config.replace_str(applicationContext_path,'${KEYSTORE_PWD}',str(keystore_pwd))
        self.config.replace_str(applicationContext_path,'${WEB3SDK_CONFIG_IP}',"127.0.0.1")
        self.config.replace_str(applicationContext_path,'${WEB3SDK_CONFIG_PORT}',str(channel_port))
        self.config.replace_str(applicationContext_path,'${WEB3SDK_SYSTEM_CONTRACT_ADDR}',DEFAULT_SYSTEM_CONTRACT_ADDRESS)
        return 0

    def bootstrapnodes_json(self,bootstrapnodes_path,p2p_port):
        '''build bootstrapnodes.json'''
        bootstrapnodes_path = bootstrapnodes_path
        os.environ['bootstrapnodes_path'] = bootstrapnodes_path
        os.system('cp ./build/tpl_dir/bootstrapnodes.json.tpl ${bootstrapnodes_path}')
        self.config.replace_str(bootstrapnodes_path,'30303',str(p2p_port))
        return 0

    

    def godminer_replace(self,godminer_path,channel_port,NODE_ID):
        '''build godminer.json'''
        godminer_path = godminer_path
        os.environ['godminer_path'] = godminer_path
        os.system('cp ./build/tpl_dir/godminer.json.tpl ${godminer_path}')  
        self.config.replace_str(godminer_path,"${GODMINERSTART_TPL}",'0')
        self.config.replace_str(godminer_path,"${GODMINEREND_TPL}","0xffffffffff")
        self.config.replace_str(godminer_path,'${PORT_TPL}',str(channel_port))
        self.config.replace_str(godminer_path,'${IDENTITYTYPE_TPL}',"1")
        self.config.replace_str(godminer_path,'${PEERIP_TPL}',"127.0.0.1")
        self.config.replace_str(godminer_path,'${AGENCYINFO_TPL}',"temp")
        self.config.replace_str(godminer_path,'${NODEDESC_TPL}',"127.0.0.1")
        self.config.replace_str(godminer_path,'${NODEID_TPL}',str(NODE_ID))
        self.config.replace_str(godminer_path,'${IDX_TPL}',"0")
        

    def node_install(self,node_id_list,gessis_json_path):
        '''install function

        mkdir build from tpl
        start temp_node
        register node_id_list from gessis_json_path
        output gessis.json
        stop temp_node
        rm build
        '''
        print("    Installing temp fisco-bcos environment start")
        os.system('cp -rf ./tpl ./build')

        cfg_ini = ConfigParser.ConfigParser()
        config_file_path="config.ini"
        cfg_ini.read(config_file_path)
        
        #chain_id need changed
        chain_id = 12345
        chain_id = chain_id +1
        p2p_port = cfg_ini.getint("ports", "p2p_port")
        rpc_port = cfg_ini.getint("ports", "rpc_port")
        channel_port = cfg_ini.getint("ports", "channel_port")
        keystore_pwd = cfg_ini.getint("web3sdk", "keystore_pwd") 
        clientcert_pwd = cfg_ini.getint("web3sdk", "clientcert_pwd")
        
        # node_id = commands.getoutput('cat /data/node.nodeid')
          
        # copy fisco-bcos
        #os.system('cp "${PATH}/fisco-bcos" ./build')
        # get bootstrapnodes.json
       
        #replace config.json
        config_path = './build/node0/config.json'
        self.config_json(config_path,rpc_port,p2p_port,channel_port,chain_id)
        

        #then start to write godInfo.txt
        os.system('./build/fisco-bcos --newaccount ./build/godInfo.txt')
        line = self.config.get_str("./build/godInfo.txt")[1]
        print(line,type(line))
        god_addr = line.split(":")[1]
        god_addr = god_addr.replace("\n","")
        print("this god is => " + god_addr)
        os.environ['god_addr'] = god_addr

        if not god_addr:
            os.environ['message']=" fisco-bcos --newaccount opr faild."
            os.system('bash ${utils}  error')
            return 1

        # replace genesis 
        os.system('cp ./build/tpl_dir/temp_node_genesis.json.tpl ./build/node0/genesis.json')
        str_nodeid = str(NODE_ID)
        self.config.get_to_write('./build/node0/genesis.json',"initMinerNodes",str_nodeid)
        print("god is => " + str(god_addr))
        self.config.get_to_write('./build/node0/genesis.json',"god" ,god_addr)
        print("generate_genesisBlock ,god => " + str(NODE_ID))


        # app.xml  make start.sh and change it same to stop.sh start_godminer.sh already do this
        applicationContext_path = './build/web3sdk/conf/applicationContext_path'
        self.application_Context_replace(applicationContext_path,clientcert_pwd,keystore_pwd,channel_port,DEFAULT_SYSTEM_CONTRACT_ADDRESS)

        print("    Waiting for temp node starting ...")
        time.sleep(5)

        os.environ['WEB3SDK_CONFIG_PORT']=str(channel_port)
        # check if temp node is running
        stat = commands.getstatusoutput('bash ${utils} check')
        if not stat[0]:
            os.environ['message']="channel port " + str(channel_port) + " is not listening, temp node start not success."
            os.system('bash ${utils} error')
            return 1
        else:
            print("channel port " + str(channel_port) + " is listening...")


        #write in godminer.json
        godminer_path="./build/node0/godminer.json"
        self.godminer_replace(godminer_path,channel_port,NODE_ID)
        syaddress = DEFAULT_SYSTEM_CONTRACT_ADDRESS
        #get syaddress to applicationContext and config.json
        print("system contract deployed ,syaddress => " + syaddress)

        os.chdir('./build/web3sdk/bin')
        node_num_per_host = len(node_id_list)
        node_num_per_host = 3
        for i in range(0,node_num_per_host):
            node_path= 'PATH '+ '_' + i + '.json'
            print(" ==== register node json =>" + node_path)
            os.environ['node_path'] = node_path
            #os.system('bash system_contract_tools.sh NodeAction registerNode file:${node_path}')
        
        print("all register node => ")
        os.system('bash system_contract_tools.sh NodeAction all')
        os.chdir('../../../')
        #output
    
        time.sleep(6)
        os.system('bash ./build/node0/stop.sh')
        gessis_json_path
        os.environ['gessis_json_path'] = gessis_json_path
        #os.system('./build/fisco-bcos --genesis ./build/node0/genesis.json  --config ./build/node0/config.json --export-genesis ${gessis_json_path}  >./build/node0/fisco-bcos.log 2>&1')
        os.system('./build/fisco-bcos --genesis ./build/node0/genesis.json  --config ./build/node0/config.json --export-genesis ./output/genesis.json  >./build/node0/fisco-bcos.log 2>&1')
        os.system('rm -rf ./build')
        print("    Installing temp node fisco-bcos success!")
        return 0






if __name__=="__main__":
    '''main function'''
    print('main')
    test = TempNode()
    node_list = ['1','2','3']
    test.node_install(node_list,'~/mydata')

   