#!/usr/bin/python


import os

FILE_PATH = './mydata' #send PATH to it
TYPE_GEN = 0

''''generate cert the copy part is not compelete we need finish this partion
'''
class CertGenerate(object):
    def __init__(self, PATH):
        self.PATH = FILE_PATH

    '''`check ca.crt exist or not'''
    def check_ca_exist(self, FILE_PATH):
        if  (os.path.isfile(FILE_PATH + '/' + 'ca.crt')&os.path.isfile(FILE_PATH + '/' + 'ca.key')):
            # do cp work function 2
            print("exist")
            return 0
        else:
            # do generate work function 1
            print("not exist")
            if os.path.exists('mydata'):
                #os.environ['var']=str(FILE_PATH)
                os.system('mkdir mydata')
            os.system('bash generate_chain_cert.sh -o ./mydata')
            return 0

    '''check agency cert exist or not'''
    def check_agency_exist(self, FILE_PATH, agency_name='test-agency'):
        # read the agency name
        AGENCY_PATH = FILE_PATH + '/' + agency_name + '/'
        if  (os.path.isfile(AGENCY_PATH + 'ca.crt')&os.path.isfile(AGENCY_PATH + 'agency.crt')&os.path.isfile(AGENCY_PATH + 'agency.key')):
            # do cp work function 2
            print("exist")
            return 0
        else:
            # do generate work function 1
            print("not exist")
            os.environ['var']=str(agency_name)
            os.system('bash generate_agency_cert.sh -c ./mydata -o ./mydata -n $var')
            return 0

    '''check sdk cert exist or not'''
    def check_sdk_exist(self, FILE_PATH, agency_name='test-agency'):
        SDK_PATH = FILE_PATH + '/' + agency_name + '/' + 'sdk' + '/'
        if  (os.path.isfile(SDK_PATH + 'ca.crt')&os.path.isfile(SDK_PATH + 'sdk.crt')&os.path.isfile(SDK_PATH + 'sdk.key')):
            # do cp work function 2
            print("exist")
            return 0
        else:
            # do generate work function 1
            print("not exist")
            os.environ['var']=str(agency_name)
            os.system('bash generate_sdk_cert.sh -d ./mydata/$var')
            return 0

    '''check nod cert exist or not'''
    def check_node_exist(self, FILE_PATH, agency_name, node_name):
        AGENCY_PATH = FILE_PATH + '/' + agency_name + '/'  # all to path
        NODE_PATH = FILE_PATH + '/'  + node_name + '/'
        if  (os.path.isfile(NODE_PATH + '/' + 'ca.crt')&os.path.isfile(NODE_PATH + '/' + 'node.ca')&os.path.isfile(NODE_PATH + '/' + 'node.key')):
            # do cp work function 2
            print("exist")
            return 0
        else:
            # do generate work function 1
            print("not exist")
            os.environ['var_agency']=str(agency_name)
            os.environ['var_node']=str(node_name)
            os.environ['var_path']=str(AGENCY_PATH)
            os.system('mkdir ./mydata/$var_node')
            os.system('bash generate_node_cert.sh -a $var_agency -d $var_path -n $var_node -o ./mydata/$var_node')
            return 0
    '''cp *.crt to where they need'''


    # '''Test shell to generate chain cert'''
    # def generate_chain_cert(self, TYPE_GEN):
    #     print("gen work")
    #     if TYPE_GEN == 'chain':
    #         os.system('./generate_chain_cert.sh -o ./mydata')
    #     return 0

    # '''  use shell to generate sdk cert    '''
    # def generate_sdk_cert(self, TYPE_GEN):
    #     print("gen work")
    #     if TYPE_GEN == 'SDK':
    #         os.system('./generate_sdk_cert.sh -o ./mydata')
    #     return 0

    # '''use shell to generate agency cert'''
    # def generate_agency_cert(self, TYPE_GEN):
    #     print("gen work")
    #     if TYPE_GEN == 'agency':
    #         os.system('./generate_agency_cert.sh -o ./mydata')
    #     return 0







#test.check_sdk_exist(FILE_PATH, agency_name='agency-test')
#check_sdk_exist(FILE_PATH, agency_name='agency-test')
if __name__=="__main__":
    print('main')
    test = CertGenerate(FILE_PATH)
    test.check_node_exist(FILE_PATH,'test-agency1','node1')
    #test.check_agency_exist(FILE_PATH, agency_name='test-agency1')
    #test.check_sdk_exist(FILE_PATH, agency_name='test-agency1')

