#!/bin/bash

###start_module###
function start_module()
{
    local package_config=$1
    local start_path=$2
    local index=$3
    ansible ${package_config} -m shell -a "bash ${start_path}/node${index}/start.sh"
}

###stop_module###
function stop_module()
{
    local package_config=$1
    local stop_path=$2
    local index=$3
    ansible ${package_config} -m shell -a "bash ${stop_path}/node${index}/stop.sh"
}



case $1 in
    start) start_module $2 $3 $4;;
    stop) stop_module $2 $3 $4;;

    *) echo "wrong command";;
esac