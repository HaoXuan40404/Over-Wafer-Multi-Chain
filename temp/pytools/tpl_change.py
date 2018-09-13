#!/usr/bin/python

import os
import sys
import commands
import json


class Json_Replace(object):
		
    def __init__(self):
		self=self

    '''get json'''
    def get_new_json(self,filepath,key,value):
        key_ = key.split(".")
        #key_ = key
        key_length = len(key_)
        with open(filepath, 'rb') as f:
            json_data = json.load(f)
            i = 0
            a = json_data
            while i < key_length :
                if i+1 == key_length :
                    a[key_[i]] = value
                    i = i + 1
                else :
                    a = a[key_[i]]
                    i = i + 1
        f.close()
        return json_data

    '''write json'''	
    def rewrite_json_file(self,filepath,json_data):
        with open(filepath, 'w') as f:
            json.dump(json_data,f)
        f.close()

    '''just use them two
	   enter the path the key whick your want to changed and the value
	'''
    def get_to_write(self,filepath,key,value):

        m_json_data = self.get_new_json(filepath,key,value)	
        self.rewrite_json_file(filepath,m_json_data)

        return 0

    '''replace file str'''
    def replace_str(self, filepath, old_str, new_str):
        f = open(filepath,'r+')
        all_lines = f.readlines()
        f.seek(0)
        f.truncate()
        for line in all_lines:
            line = line.replace(old_str, new_str)
            f.write(line)
        f.close()

    '''get file str'''
    def get_str(self, filepath):
        f = open(filepath,'r+')
        all_lines = f.readlines()
        #for line in all_lines:
        #    print(line)     
        f.close()
        return all_lines
 
'''main function'''
if __name__ == '__main__':

    os.environ['blk']='10'
    #blk = commands.getoutput('./web3sdk eth_blockNumber | grep BlockHeight | awk -F ":" "{print $2}" 2>/dev/null')
    test=Json_Replace()
    blk = commands.getoutput('echo ${blk}')
    blk = int(blk)
    print("block number is ",blk)
    blk=int(blk)+1
    print("block number is ",blk)
    blk=hex(blk)
    print("block number is ",blk)
    os.system('cp ./dependencies/tpl_dir/godminer.json.tpl ./godminer.json')
    json_path = 'applicationContext.xml'
    # m_json_data = test.get_new_json(json_path,"godMinerStart",blk)	
    # test.rewrite_json_file(json_path,m_json_data)
    test.replace_str("applicationContext.xml",'${DEFAULT_SYSTEM_CONTRACT_ADDRESS}',"syaddress")
    print("system contract deployed ,syaddress => " + "syaddress")    
    ''' get godminer.json
    test.replace_str(json_path,"${GODMINERSTART_TPL}",str(blk))
    test.replace_str(json_path,"${GODMINEREND_TPL}","0xffffffffff")
    # idx_1 = commands.getoutput('echo ${p2pport[0]}')
    # idx_2 = commands.getoutput('echo ${nodeid}')
    # idx_3 = commands.getoutput('echo ${Nodedesc}')
    # idx_4 = commands.getoutput('echo ${Agencyinfo}')
    
    idx_1 = "os.environ['echo ${p2pport[0]}']"
    idx_2 = "os.environ['echo ${nodeid}']"
    idx_3 = "os.environ['echo ${Nodedesc}']"
    idx_4 = "os.environ['echo ${Agencyinfo}']"
    test.replace_str(json_path,'${PORT_TPL}',idx_1)
    test.replace_str(json_path,'${IDENTITYTYPE_TPL}',"1")
    test.replace_str(json_path,'${PEERIP_TPL}',"127.0.0.1")
    test.replace_str(json_path,'${AGENCYINFO_TPL}',idx_4)
    test.replace_str(json_path,'${NODEDESC_TPL}',idx_3)
    test.replace_str(json_path,'${NODEID_TPL}',idx_2)
    test.replace_str(json_path,'${IDX_TPL}',"0")
    '''
    '''chmod test'''
	#os.system('touch test')
	#os.system('chmod +w test')
	
    # key = sys.argv[1]
    # value = sys.argv[2]
    # json_path = 'applicationContext.xml'
    # os.system('cd dependencies | cat config.sh')
    #os.system('')
    # os.system('cp ./dependencies/tpl_dir/start.sh.tpl ./start.sh')
    # test=Json_Replace()
    # idx="123123"
    # NODE_INSTALL_DIR="get value
    # os.environ['utils'] = './dependencies/scripts/utils.sh'
    # idx="6003"

    # os.environ['WEB3SDK_CONFIG_PORT']=idx

    # stat = commands.getstatusoutput('bash ${utils} check')
    # print("this is " +str(stat))
    # result=stat[0]
    # print(result)
    # print(len(str(commands.getstatusoutput('bash ${utils} check'))))
    # print("=====")
	 


    '''check if temp node is running'''

    # if not stat[0]:
    #     os.environ['message']="channel port " + idx + "is not listening, temp node start not success."
    #     os.system('bash ${utils}  error')
    #     print("here now is ")
    # else:
	# 	print("and here")

    #return 0
    '''test json get right or not and file changed'''
    # # test.get_to_write(json_path,"listenip.12345",999)
	# #test.rewrite_json_file(json_path,json_data)
    # os.system('cp ./dependencies/tpl_dir/applicationContext.xml.tpl ./applicationContext.xml')
    # #json_path = app.xml path
    # '''${CLIENTCERT_PWD}:${KEYSTORE_PWD}:${WEB3SDK_CONFIG_IP}:${WEB3SDK_CONFIG_PORT}:${WEB3SDK_SYSTEM_CONTRACT_ADDR}'''
    # test.replace_str(json_path,'${CLIENTCERT_PWD}',idx)
    # test.replace_str(json_path,'${KEYSTORE_PWD}',idx)
    # test.replace_str(json_path,'${WEB3SDK_CONFIG_IP}',idx)
    # test.replace_str(json_path,'${WEB3SDK_CONFIG_PORT}',idx)
    # test.replace_str(json_path,'${WEB3SDK_SYSTEM_CONTRACT_ADDR}',idx)

    
    	
    #test.get_to_write(json_path,"wallet","666")
    # m_json_data = test.get_new_json(json_path,"wallet",999)	
    # test.rewrite_json_file(json_path,m_json_data)





'''file test'''
# with open('config.json.test') as conf:
#     for line in conf():
#         if re.search('${CONFIG_JSON_SYSTEM_CONTRACT_ADDRESS_TPL}',line):
#             line = re.sub('${CONFIG_JSON_SYSTEM_CONTRACT_ADDRESS_TPL}','test_var_1',line)
#             w_str+=line
#         else:
#             w_str+=line
# print w_str
# conf.close


    # line = conf.readline()
# with open(filename, 'r+') as conf:
#     # for line in conf:
#     #     _json = json.loads(line)
#     pop_data = json.load(conf)
#     print(type(pop_data))
#     #data = "cryptomod" + ":" + "12"
#     _json = json.dumps(pop_data['cryptomod'])
#     print(type(pop_data['cryptomod']))
#     print(type(_json))
#     print(_json)
#     json.dump(['cryptomod':'123'],conf)
#     print(pop_data['cryptomod'])

   

# conf.close()


