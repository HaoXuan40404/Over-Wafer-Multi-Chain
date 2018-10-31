#!/bin/bash
source /etc/profile
dirpath="$(cd "$(dirname "$0")" && pwd)"
cd $dirpath
 
index=$1

function error()
{
    echo "ERROR! $1"; exit 0;
}

function check_file()
{
    file=$1
    if [ ! -f ${file} ];then
        error "${file} is not exist."
    fi
}

function register_or_not()
{
    local nodeid=$1
    ret=$(bash web3sdk/bin/web3sdk NodeAction all 2> /dev/null)
    if [ $? -eq 0 ];then
        error " NodeAction all operation failed."
    fi

    if echo $ret | egrep $nodeid >/dev/null 2>&1;then
        return 0
    fi
    return 1
}

nodefile=node$index/data/node.json
configfile=node$index/config.json
nodeidfile=node$index/data/node.nodeid
check_file $nodefile
check_file $configfile
check_file $nodeidfile

# check if fisco is syncing
config_ip=$(cat $configfile |grep -o '"listenip": ".*"' | grep -o "[0-9]\+\.[0-9]\+\.[0-9]\+\.[0-9]\+")
config_port=$(cat $configfile |grep -o '"rpcport": ".*"' | grep -o "[0-9]\+")
result=$(curl -s  "http://$config_ip:$config_port" -X POST --data '{"jsonrpc":"2.0","method":"eth_syncing","params":[],"id":1}')
[ -z "$result" ] &&  {
    error " Cannot connect to $config_ip:$config_port."
    }

echo "$result" | egrep "false" >/dev/null 2>&1
[ $? -ne 0 ] && {
    error " node${index} is eth_syncing."
}

nodeid=$(cat `pwd`/node$index/data/node.nodeid)
register_or_not $nodeid
if [ $? -eq 0 ];then
    echo " OK! $node has been registered."; exit 0;
fi

# https://github.com/ethereum/wiki/wiki/JSON-RPC#eth_syncing
bash web3sdk/bin/web3sdk NodeAction registerNode file:`pwd`/node$index/data/node.json
if [ $? -ne 0 ];then
    error " NodeAction registerNode opr failed."
fi

index=0
while $index -lt 10
do
    register_or_not $nodeid
    if [ $? -eq 0 ];then
        echo " OK! register $node success."; exit 0;
    fi
    sleep 3
done

error " register $node timeout..."
