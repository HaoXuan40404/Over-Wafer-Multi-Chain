#!/usr/bin/python

import os
import commands
import sys
sys.path.append('./pytools')
import tpl_change
import time
import ConfigParser


class TempNode(object):
    
    def __init__(self, PWD):
        self.PWD = PWD
        global DEFAULT_SYSTEM_CONTRACT_ADDRESS
        DEFAULT_SYSTEM_CONTRACT_ADDRESS="0x919868496524eedc26dbb81915fa1547a20f8998"

    '''install function'''
    def install(self):
        print("    Installing temp fisco-bcos environment start")
        os.system('cp -rf ./tpl ./build')
        config=tpl_change.Json_Replace()
        # node_id = commands.getoutput('cat ${installPWD}/data/node.nodeid')
        node_id = "8c0fbe3a9b31775fc9786d7ae791e72b299d71bec18f18eb908caf637c71eaab4c691e738c41bc03478dd262077230056a4b0f07e9043445ea5632560326b8f5"


        # copy fisco-bcos
        #os.system('cp "${PATH}/fisco-bcos" ./build')
        # get bootstrapnodes.json
       
        #replace config.json  ###########################      
        os.system('cp ./build/tpl_dir/config.json.tpl ./build/node0/config.json')
        cfg_ini = ConfigParser.ConfigParser()
        config_file_path="config.ini"
        cfg_ini.read(config_file_path)
        
        '''chain_id need changed'''
        chain_id = 12345
        chain_id = chain_id +1
        p2p_port = cfg_ini.getint("ports", "p2p_port")
        rpc_port = cfg_ini.getint("ports", "rpc_port")
        channel_port = cfg_ini.getint("ports", "channel_port")
        keystore_pwd = cfg_ini.getint("web3sdk", "keystore_pwd") 
        clientcert_pwd = cfg_ini.getint("web3sdk", "clientcert_pwd")
        # nodes = cfg_ini.get("nodes", "node0")
        #  = nodes.split()
        config.get_to_write('./build/node0/config.json',"systemproxyaddress",DEFAULT_SYSTEM_CONTRACT_ADDRESS)
        config.get_to_write('./build/node0/config.json',"listenip","127.0.0.1")
        config.get_to_write('./build/node0/config.json',"cryptomod","0")
        config.get_to_write('./build/node0/config.json',"rpcport",str(rpc_port))
        config.get_to_write('./build/node0/config.json',"p2pport",str(p2p_port))
        config.get_to_write('./build/node0/config.json',"channelPort",str(channel_port))
        config.get_to_write('./build/node0/config.json',"wallet","./build/node0/keys.info")
        config.get_to_write('./build/node0/config.json',"keystoredir","./build/node0/keystore")
        config.get_to_write('./build/node0/config.json',"datadir","./build/node0/data")
        config.get_to_write('./build/node0/config.json',"networkid",str(chain_id))
        config.get_to_write('./build/node0/config.json',"logconf","./log.conf")

        #then start to write godInfo.txt
        os.system('./build/fisco-bcos --newaccount ./build/godInfo.txt')
        line = config.get_str("./build/godInfo.txt")[1]
        print(line,type(line))
        god_addr = line.split(":")[1]
        god_addr = god_addr.replace("\n","")
        print("this god is => " + god_addr)
        os.environ['god_addr'] = god_addr

        if not god_addr:
            os.environ['message']=" fisco-bcos --newaccount opr faild."
            os.system('bash ${utils}  error')
            return 1

        #replace genesis ###########################
        config=tpl_change.Json_Replace()
        os.system('cp ./build/tpl_dir/temp_node_genesis.json.tpl ./build/node0/genesis.json')
        str_nodeid = [str(node_id)]
        config.get_to_write('./build/node0/genesis.json',"initMinerNodes",str_nodeid)
        print("god is => " + str(god_addr))
        config.get_to_write('./build/node0/genesis.json',"god" ,god_addr)
        print("generate_genesisBlock ,god => " + str(node_id))


        # app.xml  make start.sh and change it same to stop.sh start_godminer.sh already do this
        os.system('cp ./build/tpl_dir/applicationContext.xml.tpl ./build/web3sdk/conf/applicationContext.xml')
        config.replace_str('./build/web3sdk/conf/applicationContext.xml','${CLIENTCERT_PWD}',str(clientcert_pwd))
        config.replace_str('./build/web3sdk/conf/applicationContext.xml','${KEYSTORE_PWD}',str(keystore_pwd))
        config.replace_str('./build/web3sdk/conf/applicationContext.xml','${WEB3SDK_CONFIG_IP}',"127.0.0.1")
        config.replace_str('./build/web3sdk/conf/applicationContext.xml','${WEB3SDK_CONFIG_PORT}',str(channel_port))
        config.replace_str('./build/web3sdk/conf/applicationContext.xml','${WEB3SDK_SYSTEM_CONTRACT_ADDR}',DEFAULT_SYSTEM_CONTRACT_ADDRESS)

        os.system('chmod +x ./build/node0/start_godminer.sh')
        os.system('chmod +x ./build/node0/start.sh')
        os.system('chmod +x ./build/node0/stop.sh')
        os.system('bash ./build/node0/start.sh')

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
        os.system('cp ./build/tpl_dir/godminer.json.tpl ./build/node0/godminer.json')
        json_path="./build/node0/godminer.json"
        config.replace_str(json_path,"${GODMINERSTART_TPL}",'0')
        config.replace_str(json_path,"${GODMINEREND_TPL}","0xffffffffff")
        config.replace_str(json_path,'${PORT_TPL}',str(channel_port))
        config.replace_str(json_path,'${IDENTITYTYPE_TPL}',"1")
        config.replace_str(json_path,'${PEERIP_TPL}',"127.0.0.1")
        config.replace_str(json_path,'${AGENCYINFO_TPL}',"temp")
        config.replace_str(json_path,'${NODEDESC_TPL}',"127.0.0.1")
        config.replace_str(json_path,'${NODEID_TPL}',str(node_id))
        config.replace_str(json_path,'${IDX_TPL}',"0")
        syaddress = DEFAULT_SYSTEM_CONTRACT_ADDRESS
        #get syaddress to applicationContext and config.json
        print("system contract deployed ,syaddress => " + str(god_addr))
        config.replace_str("./build/web3sdk/conf/applicationContext.xml",str(god_addr),syaddress)
        print("system contract deployed ,syaddress => " + syaddress)

        config.replace_str("./build/node0/config.json",DEFAULT_SYSTEM_CONTRACT_ADDRESS,syaddress)

        os.chdir('./build/web3sdk/bin')

 
        node_num_per_host = 3
        for j in range(0,node_num_per_host):
            node_index=str(j)
            node_path= 'PATH=' + "$public_ip_underline" + '_' + node_index + '.json'
            print(" ==== register node json =>" + node_path)
            os.environ['node_path'] = node_path
            #os.system('bash system_contract_tools.sh NodeAction registerNode file:${node_path}')
        
        print("all register node => ")
        os.system('bash system_contract_tools.sh NodeAction all')
        os.chdir('../../../')
        #output
        os.system('./build fisco-bcos --genesis ./build/node0/  --config ./build/node0/config.json --export-genesis ./output/genesis.json  >./build/node0/fisco-bcos.log 2>&1')
        #./fisco-bcos  --genesis $installation_build_dir/$TEMP_NODE_NAME/build/node0/genesis.json  --config $installation_build_dir/$TEMP_NODE_NAME/build/node0/config.json --export-genesis $TEMP_BUILD_DIR/genesis.json  >$installation_build_dir/$TEMP_NODE_NAME/build/node0/fisco-bcos.log 2>&1

        time.sleep(6)
        os.system('bash ./build/node0/stop.sh')
        os.system('rm -rf ./build')

        print("    Installing temp node fisco-bcos success!")

        return 0





'''main function'''
if __name__=="__main__":
    print('main')
    test = TempNode('')
    test.install()

   