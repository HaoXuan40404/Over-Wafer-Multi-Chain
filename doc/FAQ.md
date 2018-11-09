# FAQ
常问问题

## 系统环境错误

- yum install https://dl.fedoraproject.org/pub/epel/epel-release-latest-7.noarch.rpm 失败

yum源出现问题，请确定yum源正常
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
- ERROR | OWMC init fault
  
多链初始化失败，请从新尝试clone代码

- ERROR | invalid opr,  \"python main.py -h\" can be used to show detailed usage.

用户命令输入错误，请检查命令

- ERROR | main.py: error: unrecognized arguments: 

命令参数输入不匹配，参数过多，请检查参数是否符合输入标准

- ERROR | main.py: error: argument --XXX  expected n argument(s)
  
命令参数输入不匹配，参数不足，请检查参数是否符合输入标准

- ERROR | ansible XXX fiailed XXX | FAILED！ => XXX Permission denied XXX
  
用户所处用户组没有权限对mchain.conf中部署目录dir进行操作，请更换目录，或增加对应服务器相应目录权限。

- ERROR | ansible XXX fiailed  host is XXX, output is XXX | FAILED！ => XXX Warning: Permanently added XXX
- ERROR | ansible XXX fiailed  host is XXX, output is XXX | FAILED！ => XXX Failed to connect to the host via ssh :Permission denied(publickey,password) XXX
  
hostip对应服务器命令执行错误，请检查错误结果，对应failed描述，检查ansible配置文件。用户没有成功配置ssh密钥，请尝试检查ansible配置，并运行ansible配置中的相应脚本

- ERROR | ansible XXX fiailed  host is XXX, output is XXX| FAILED！ => XXX SSH Error: data could not be sent to remote host XXX

hostip对应服务器命令执行错误，请检查错误结果，对应failed描述，用户无法与对应服务器进行ssh通信，请检查/etc/ansible/hosts中的配置是否正确，并检查/etc/ansible/ansible.cfg中的相关配置是否完成

- ERROR -  rpc port check, XXX is in use
- ERROR -  channel port check, XXX is in use
- ERROR -  p2p port check, XXX is in use
  
rpc/channel/p2p port被占用，请尝试修改端口号从新进行安装。

- ERROR | syntax error unexpected end of file
- ERROR | 语法错误 未预期的文件结尾

format.sh脚本执行失败，请尝试从新进行部署或手动将文件转义成unix
## build命令错误
- ERROR | fisco-bcos is not exist, path is XXX

用户指定的fisco-bcos文件不存在，XXXXXX为用户输入的路径。请确定该路径，并指定正确的fisco-bcos在本机上的路径位置

- ERROR | invalid config format parser failed, config is XXX, exp is XXX

用户输入的.conf文件解析失败，请确认指定conf/文件夹下没有其他文件

- ERROR | chain_id XXX and chain_version XXX config repeat.

用户在conf文件中指定的chain_id和chain_version重复，请解决冲突

- ERROR | skip config XXX, invalid config format parser failed

用户在conf文件夹下的XXX文件错误，请检查该文件格式是否正确，如果用户在多链物料包conf文件夹下进行操作，则在解析mchain.conf和logging.conf会出现两次错误，可忽略

- ERROR | invalid config, neither directory nor file, config is XXX

用户指定conf文件或者conf文件夹错误，请检查输入的指令

- ERROR | build install package for chain version failed, data dir aleady exist

用户指定的该版本号的该链存在，请检查是否之前配置过该链

- ERROR | build install package for chain 12345 version v1.0.0 failed, exception is temp node start failed.

temp节点启动失败，端口号被占用，请检查sample.conf文件的端口号配置

- ERROR | chain XXX host XXX, publish install package failed

用户在hosts.conf指定的用户在对应服务器无法访问mchain.conf中dir的路径，请确认dir是否配置正确，或者给予权限。

## publish命令错误

- ERROR | skip, invalid publish format, chain_id:chain_version should require, chain is XXX

用户发布时必须输入chainid和版本号，中间用“：”隔开，请确认输入是否正确

- ERROR | publish install package for chain version failed, data dir not exist

用户指定发布的链不存在，请检查输入是否正确

- ERROR | chain XXX already publish XXX version, if you want publish annother version, --force/-f need to be set.

用户指定发布的链已经发布过，如果需要强制发布请尝试组合使用-f命令

- ERROR | push package : XXX  failed

publish安装包失败，请检查网络环境
## 参数输入错误

- ERROR | Input is invalid, Exception XXX

用户参数输入错误，请检查输入参数是否合法
- ERROR | XXXchain_resolve error, XXX is not a valid chain_id

用户输入chain_id不符合标准，chain_id仅能为整形
- ERROR |X_chain_resolve type error, chain[X] =>'  chain[X]
- 
用户输入的第X个参数不合法，请检查输入
- ERROR | skip host XXX, invalid ip format

用户输入的hostip XXX不合法，请检查输入

## 操作执行错误

- ERROR | ansible telnet failed，host is XXX，output is XXX
- ERROR | ansible cmd failed，host is XXX，output is XXX
- ERROR | ansible diagnose failed，host is XXX，output is XXX
  
ansible通信失败，请确定host.conf文件配置是否正确，并且正确执行了--init命令，或是已经允许ssh通信。

- ERROR | Generate XXX cert failed! Cant find cert in XXX.
  
证书生成失败，无法再对应目录下找到需要生成证书的依赖文件，请确认指定的文件夹内证书完整。

- ERROR | Generate XXX cert failed! Please check your network, and try to check your opennssl version.

证书生成失败，请确认本机安装的opennssl版本正确，并能正常与opennssl进行请求。
  
- ERROR | Init cert failed! files not completed

证书初始化失败，指定的证书不完整

- ERROR | skip config XXX, invalid config format parser failed, exception is XXX 

指定的conf文件配置格式错误

- ERROR | No package build for chain_id(XXX):chain_version(XXX).

用户导出的包不存在，请确定build成功，并且参数输入正确

- ERROR | Not invalid chain_id, chain_id is XXX
  
导出时输入的chain_id格式错误


- ERROR | chain not published
  
操作的链尚未发布，请发布后再次进行操作

 - ERROR | register failed, XXX

注册节点失败，请检查网络环境，是否正确连接到对应服务器。

 - ERROR | register failed, chain_id is XXX, host is XXX, node is XXX.

注册节点失败，请检查网络设置。

- ERROR | unregister failed, XXX

踢出节点失败，请检查网络环境，是否正确连接到对应服务器。

- ERROR | unregister failed, chain_id is XXX, host is XXX, node is XXX

踢出节点失败，请检查网络设置。

- ERROR | Not invalid host, skip, host is XXX

telnet命令失败，输入的hostip不合法

- ERROR | invalid docmd dst, dst is XXX, dst should be invalid chain_id or invali host ip or 'all'

cmd命令对应操作路径错误，请检查对应操作路径

- ERROR | src is not exist, src is XXX.

pushfile中本地的文件不存在，请检查路径是否正确

- ERROR | invalid push file host, host is XXX, dst should be invalid chain_id or invali host ip or 'all'

pushfile命令对应操作路径错误，请检查对应操作路径