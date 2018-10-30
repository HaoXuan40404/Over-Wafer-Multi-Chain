#!/bin/bash
dirpath="$(cd "$(dirname "$0")" && pwd)"
cd $dirpath

# check if file exist, if not shell will exit with 1 returncode.
function check_file()
{
    file=$1
    if [ ! -f ${file} ];then
        echo " ${file} is not exist."
        exit 1
    fi
}

# echo with ip、time ahead
function alarm()
{
    alert_ip=`/sbin/ifconfig eth0 | grep inet | awk '{print $2}'`
    time=`date "+%Y-%m-%d %H:%M:%S"`
    echo "$alert_ip $1";
}

# check if blockchain consensus properly
function consensus_diagnose()
{
    # checkout if file exist.
    configfile=$dirpath/config.json
    check_file config.json
    config_ip=$(cat $configfile |grep -o '"listenip": ".*"' | grep -o "[0-9]\+\.[0-9]\+\.[0-9]\+\.[0-9]\+")
    config_port=$(cat $configfile |grep -o '"rpcport": ".*"' | grep -o "[0-9]\+")

    heightresult=$(curl -s  "http://$config_ip:$config_port" -X POST --data '{"jsonrpc":"2.0","method":"eth_blockNumber","params":[],"id":67}')
    # echo $heightresult
    height=$(echo $heightresult|awk -F'"' '{if($2=="id" && $4=="jsonrpc" && $8=="result") {print $10}}')
    [ -z "$height" ] &&  {
        alarm " ERROR! Cannot connect to $config_ip:$config_port $heightresult"; 
        exit 1;
    }

    # heightvalue=$(printf "%d\n" "$height")
    viewresult=$(curl -s  "http://$config_ip:$config_port" -X POST --data '{"jsonrpc":"2.0","method":"eth_pbftView","params":[],"id":68}')
    # echo $viewresult
    view=$(echo $viewresult|awk -F'"' '{if($2=="id" && $4=="jsonrpc" && $8=="result") {print $10}}')
    [ -z "$view" ] &&  {
        alarm " ERROR! Cannot connect to $config_ip:$config_port $viewresult"; 
        exit 1;
    }

    # get PBFT view
    viewvalue=$(printf "%d\n" "$view")

    alarm " height is $height and is view $view"
}

# diagnose why node not start success.
function running_diagnose()
{
    # checkout if file exist.
    configfile=$dirpath/config.json
    check_file config.json

    node=$(basename ${dirpath})

    # check if fisco-bcos is running.
    fisco_pid=`ps aux|grep "${configfile}"|grep "fisco-bcos"|grep -v grep|awk '{print $2}'`
    if [ ! -z $fisco_pid ];then
        alarm " ${node} is running."
        consensus_diagnose
        return 
    fi

    alarm " ${node} is not running, start ${node}."

    # start node again
    bash $dirpath/start.sh
    sleep 10
    # check if fisco-bcos is running.
    fisco_pid=`ps aux|grep "${configfile}"|grep "fisco-bcos"|grep -v grep|awk '{print $2}'`
    if [ ! -z $fisco_pid ];then
        alarm " start success, ${node} is running now."
        consensus_diagnose
        return
    fi 

    # find why node start failed?
    alarm " => diagnose running begin ."

    # check if core file exist.
    core_file_c=$(ls -lt core* | wc | awk '{print $1}')
    if [ ${core_file_c} -gt 1 ];then
        alarm "   => core file list :"
        ls -lt $dirpath/core* | awk '{print $9}' 
    fi

    # first log out log/log file content.
    if [ -s $dirpath/log/log ];then
        alarm "   => log/log file content is "$(cat $dirpath/log/log)
    fi

    # find out last log file, and show out last 10 ERROR print.
    if [ ! -d $dirpath/log ];then
        alarm "   => error log : "
        ls -lt log/log*.log | awk '{print $9}' | head -1 | xargs egrep "ERROR" | tail -10
    else
        alarm "log dir not exist, dir is ${dirpath}/log"
    fi
}

# node index
node=$(basename ${PWD})

# check if ${node}/config.json exist.
configfile=${PWD}/config.json
check_file ${configfile}

config_ip=$(cat $configfile |grep -o '"listenip": ".*"' | grep -o "[0-9]\+\.[0-9]\+\.[0-9]\+\.[0-9]\+")
config_port=$(cat $configfile |grep -o '"rpcport": ".*"' | grep -o "[0-9]\+")

# first check if fisco-bcos is running.
weth_pid=`ps aux|grep "${configfile}"|grep "fisco-bcos"|grep -v grep|awk '{print $2}'`
if [ ! -z $weth_pid ];then
    message "${node} is running."
else
    alarm "ERROR : ${node} is not running."
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
        alarm "ERROR! Cannot connect to $config_ip:$config_port $heightresult"
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
            alarm "ERROR! Cannot connect to $config_ip:$config_port $viewresult"
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
    alarm "ERROR! $config_ip:$config_port is not working properly: height $height and view $view no change"
}

echo $height > $height_file
echo $view > $view_file
message "OK! $config_ip:$config_port is working properly: height $height view $view" 