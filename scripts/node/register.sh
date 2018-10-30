#!/bin/bash
dirpath="$(cd "$(dirname "$0")" && pwd)"
cd $dirpath
 
index=$1

function check_file()
{
    file=$1
    if [ ! -f ${file} ];then
        echo " ERROR! ${file} is not exist."
        exit 1
    fi
}

nodefile=node$index/data/node.json
configfile=node$index/config.json
check_file $nodefile
check_file $configfile

# check if fisco is syncing
config_ip=$(cat $configfile |grep -o '"listenip": ".*"' | grep -o "[0-9]\+\.[0-9]\+\.[0-9]\+\.[0-9]\+")
config_port=$(cat $configfile |grep -o '"rpcport": ".*"' | grep -o "[0-9]\+")
result=$(curl -s  "http://$config_ip:$config_port" -X POST --data '{"jsonrpc":"2.0","method":"eth_syncing","params":[],"id":1}')
[ -z "$result" ] &&  {
    echo "ERROR! Cannot connect to $config_ip:$config_port."; exit 1;
    }
if echo "$result" | egrep "false";then
    # https://github.com/ethereum/wiki/wiki/JSON-RPC#eth_syncing
    bash web3sdk/bin/web3sdk NodeAction registerNode file:`pwd`/node$index/data/node.json
else
    echo " ERROR! node${index} is eth_syncing."; exit 1;
fi