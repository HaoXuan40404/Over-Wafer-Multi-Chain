#!/bin/bash
dirpath="$(cd "$(dirname "$0")" && pwd)"
cd $dirpath

function check_file()
{
    file=$1
    if [ ! -f ${file} ];then
        echo " ${file} is not exist."
        exit 0
    fi
}

function message()
{
    echo [$(date '+%F %T')]"$1"
}

function alarm()
{
        alert_ip=`/sbin/ifconfig eth0 | grep inet | awk '{print $2}'`
        time=`date "+%Y-%m-%d %H:%M:%S"`
        echo "$alert_ip $1"; exit 0;
}

function restart() 
{
        stopfile=${1/start/stop}
        bash $stopfile
        sleep 3
        bash $startfile
}

node=$(basename ${PWD})
configfile=${PWD}/config.json
check_file ${configfile}
config_ip=$(cat $configfile |grep -o '"listenip": ".*"' | grep -o "[0-9]\+\.[0-9]\+\.[0-9]\+\.[0-9]\+")
config_port=$(cat $configfile |grep -o '"rpcport": ".*"' | grep -o "[0-9]\+")
# first check if fisco-bcos is running.
weth_pid=`ps aux|grep "${configfile}"|grep "fisco-bcos"|grep -v grep|awk '{print $2}'`
if [ ! -z $weth_pid ];then
    echo " ${node} is running."
else
    echo " ${node} is not running."; exit 0;
fi

# get blocknumber
config_ip=$(cat $configfile |grep -o '"listenip": ".*"' | grep -o "[0-9]\+\.[0-9]\+\.[0-9]\+\.[0-9]\+")
config_port=$(cat $configfile |grep -o '"rpcport": ".*"' | grep -o "[0-9]\+")
for((i=0;i<3;i++))
do 
    heightresult=$(curl -s  "http://$config_ip:$config_port" -X POST --data '{"jsonrpc":"2.0","method":"eth_blockNumber","params":[],"id":67}')
    # echo $heightresult
    height=$(echo $heightresult|awk -F'"' '{if($2=="id" && $4=="jsonrpc" && $8=="result") {print $10}}')
    [[ -z "$height" && $i -eq 2 ]] &&  {
        echo " ERROR! Cannot connect to $config_ip:$config_port $heightresult"
    }
    configdir=$(dirname $configfile)
    height_file="$configdir/node.height"
    prev_height=0
    [ -f $height_file ] && prev_height=$(cat $height_file)
    heightvalue=$(printf "%d\n" "$height")
    prev_heightvalue=$(printf "%d\n" "$prev_height")

    viewresult=$(curl -s  "http://$config_ip:$config_port" -X POST --data '{"jsonrpc":"2.0","method":"eth_pbftView","params":[],"id":68}')
    # echo $viewresult
    view=$(echo $viewresult|awk -F'"' '{if($2=="id" && $4=="jsonrpc" && $8=="result") {print $10}}')
    [[ -z "$view" && $i -eq 2 ]] &&  {
            echo " ERROR! Cannot connect to $config_ip:$config_port $viewresult"
    }

    [[ -n "$height" && -n "$view" ]] && { 
            break 
    }
    sleep 1
done

# get PBFT view
view_file="$configdir/node.view"
prev_view=0
[ -f $view_file ] && prev_view=$(cat $view_file)
viewvalue=$(printf "%d\n" "$view")
prev_viewvalue=$(printf "%d\n" "$prev_view")

# check if PBFT work properly.
[  $heightvalue -eq  $prev_heightvalue ] && [ $viewvalue -eq  $prev_viewvalue ] && {
    echo " ERROR! $config_ip:$config_port is not working properly: height $height and view $view no change"
}

echo $height > $height_file
echo $view > $view_file
echo " OK! $config_ip:$config_port is working properly: height $height view $view" 