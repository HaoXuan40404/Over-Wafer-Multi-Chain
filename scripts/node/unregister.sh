#!/bin/bash
source /etc/profile
index=$1
dirpath="$(cd "$(dirname "$0")" && pwd)"
cd $dirpath

function error()
{
    echo "ERROR! $1"; exit 0;
}

function check_file()
{
    file=$1
    if [ ! -f ${file} ];then
        error " ${file} is not exist."
    fi
}

function register_or_not()
{
    local nodeid=$1
    ret=$(bash web3sdk/bin/web3sdk NodeAction all 2> /dev/null)
    if [ $? -ne 0 ];then
        error " NodeAction all operation failed."
    fi

    if echo $ret | egrep $nodeid >/dev/null 2>&1 ;then
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

nodeid=$(cat `pwd`/node$index/data/node.nodeid)
register_or_not $nodeid
if [ $? -ne 0 ];then
    echo " OK! node$index has not been registered."; exit 0;
fi

# check java version
bash scripts/tools/deps.sh java_check

bash web3sdk/bin/web3sdk NodeAction cancelNode file:`pwd`/node$index/data/node.json
if [ $? -ne 0 ];then
    error " NodeAction cancelNode operation failed."
fi

index=0
while [ $index -lt 10 ]
do
    register_or_not $nodeid
    if [ $? -ne 0 ];then
        echo " OK! unregister node$index success."; exit 0;
    fi
    sleep 3
    let index++
done

error " unregister node$index timeout..."