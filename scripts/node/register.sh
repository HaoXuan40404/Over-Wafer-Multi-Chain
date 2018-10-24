 #echo "start node$index ... "
source /etc/profile 
dirpath="$(cd "$(dirname "$0")" && pwd)"
cd $dirpath
 
index=$1

if [ -d node$index ] && [ -f node$index/data/node.json ];then
    # result=$(curl -s  "http://$config_ip:$config_port" -X POST --data '{"jsonrpc":"2.0","method":"eth_syncing","params":[],"id":1}')
    # [[ -z "$height" && $i -eq 2 ]] &&  {
    #                    alarm "ERROR! Cannot connect to $config_ip:$config_port $heightresult"
    # https://github.com/ethereum/wiki/wiki/JSON-RPC#eth_syncing
    
                }
    bash web3sdk/bin/web3sdk NodeAction registerNode file:`pwd`/node$index/data/node.json
else
    echo "node$index/node.json is node exist."
    exit 1
fi