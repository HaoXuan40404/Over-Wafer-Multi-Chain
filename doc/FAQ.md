# FAQ

## 系统环境错误
- ERROR - Unsupported or unidentified Linux distro.  

当前linux系统不支持, 目前FISCO-BCOS支持CentOS 7.2+、Ubuntu 16.04。
- ERROR -Unsupported or unidentified operating system.
  
当前系统不支持, 目前FISCO-BCOS支持CentOS 7.2+、Ubuntu 16.04。
- ERROR - Unsupported Ubuntu Version. At least 16.04 is required.  
  
当前ubuntu版本不支持, 目前ubuntu版本仅支持ubuntu 16.04 64位操作系统。
- ERROR - Unsupported CentOS Version. At least 7.2 is required.  
  
当前CentOS系统不支持, 目前CentOS支持7.2+ 64位。
- ERROR - Unsupported Oracle Linux, At least 7.4 Oracle Linux is required.  

当前CentOS系统不支持，目前CentOS支持7.2+ 64位。
- ERROR - unable to determine CentOS Version

当前CentOS系统不支持, 目前CentOS支持7.2+ 64位。
- ERROR - Unsupported Linux distribution.

不支持的linux系统.目前FISCO-BCOS支持CentOS 7.2+、Ubuntu 16.04。
- ERROR - Oracle JDK 1.8 be requied  

需要安装Oracle JDK 1.8。目前物料包的web3sdk仅支持Oracle JDK1.8版本，尚未支持其他的java版本，请参考[物料包java安装](https://fisco-bcos-test.readthedocs.io/zh/latest/docs/tools/oracle_java.html)
- ERROR - OpenSSL 1.0.2 be requied  
  
物料包需要openssl 1.0.2版本，请升级openssl版本。
- ERROR - failed to get openssl version
  
无法获取openssl的版本，请尝试从新安装openssl。 
- ERROR - XXX is not installed. 
   
XXX没有安装，请尝试安装该依赖。
- ERROR - FISCO BCOS gm version not support yet.  
  
物料包不支持国密版本的FISCO BCOS的安装。
- ERROR - At least FISCO-BCOS 1.3.0 is required.  
  
物料包工具支持的FISCO BCOS的版本最低为v1.3.0。
## 配置错误
- ERROR | invalid opr,  \"python main.py -h\" can be used to show detailed usage.

用户命令输入错误，请检查命令

- ERROR | main.py: error: unrecognized arguments: 

命令参数输入不匹配，参数过多，请检查参数是否符合输入标准

- ERROR | main.py: error: argument --***  expected n argument(s)
  
命令参数输入不匹配，参数不足，请检查参数是否符合输入标准

- ERROR | ansible *** fiailed *** | FAILED！ => *** Permission denied ***
  
用户所处用户组没有权限对mchain.conf中部署目录dir进行操作，请更换目录，或增加对应服务器相应目录权限。

- ERROR | ansible *** fiailed  host is ***, output is *** | FAILED！ => *** Warning: Permanently added ***
- ERROR | ansible *** fiailed  host is ***, output is *** | FAILED！ => *** Failed to connect to the host via ssh :Permission denied(publickey,password) ***
  
hostip对应服务器命令执行错误，请检查错误结果，对应failed描述，检查ansible配置文件。用户没有成功配置ssh密钥，请尝试检查ansible配置，并运行ansible配置中的相应脚本

- ERROR | ansible *** fiailed  host is ***, output is ***| FAILED！ => *** SSH Error: data could not be sent to remote host ***

hostip对应服务器命令执行错误，请检查错误结果，对应failed描述，用户无法与对应服务器进行ssh通信，请检查/etc/ansible/hosts中的配置是否正确，并检查/etc/ansible/ansible.cfg中的相关配置是否完成

- ERROR -  rpc port check, *** is in use
- ERROR -  channel port check, *** is in use
- ERROR -  p2p port check, *** is in use
  
rpc/channel/p2p port被占用，请尝试修改端口号从新进行安装。

## build命令错误
- ERROR | fisco-bcos is not exist, path is ******

用户指定的fisco-bcos文件不存在，******为用户输入的路径。请确定该路径，并指定正确的fisco-bcos在本机上的路径位置

- ERROR | invalid config format parser failed, config is***, exp is ***

用户输入的.conf文件解析失败，请确认指定conf/文件夹下没有其他文件

- ERROR | chain_id *** and chain_version *** config repeat.

用户在conf文件中指定的chain_id和chain_version重复，请解决冲突

- ERROR | skip config **, invalid config format parser failed

用户在conf文件夹下的**文件错误，请检查该文件格式是否正确，如果用户在多链物料包conf文件夹下进行操作，则在解析mchain.conf和logging.conf会出现两次错误，可忽略

- ERROR | invalid config, neither directory nor file, config is ***

用户指定conf文件或者conf文件夹错误，请检查输入的指令

- ERROR | build install package for chain version failed, data dir aleady exist

用户指定的该版本号的该链存在，请检查是否之前配置过该链

## publish命令错误

- ERROR | skip, invalid publish format, chain_id:chain_version should require, chain is **

用户发布时必须输入chainid和版本号，中间用“：”隔开，请确认输入是否正确
- ERROR | publish install package for chain version failed, data dir not exist

用户指定发布的链不存在，请检查输入是否正确
## 参数输入错误

- ERROR | Input is invalid, Exception **

用户参数输入错误，请检查输入参数是否合法
- ERROR | ***chain_resolve error, ** is not a valid chain_id

用户输入chain_id不符合标准，chain_id仅能为整形
- ERROR |*_chain_resolve type error, chain[*] =>'  chain[*]
- 
用户输入的第*个参数不合法，请检查输入
- ERROR | skip host **, invalid ip format

用户输入的hostip **不合法，请检查输入











