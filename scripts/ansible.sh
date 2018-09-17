#!/bin/bash
#copy_module
function copy_module()
{
    local package_config=$1
    local ansible_src=$2
    local ansible_dest=$3
    ansible ${package_config} -m copy -a "src=${ansible_src} dest=${ansible_dest}"
}

###unarchive_module###
function unarchive_module()
{
    local package_config=$1
    local ansible_src=$2
    local ansible_dest=$3
    ansible ${package_config} -m unarchive -a "src=${ansible_src} dest=${ansible_dest}, mode=0755 copy=yes"
}

###build_module###
function build_module()
{
    local package_config=$1
    local make_dir=$2
    ansible ${package_config} -m shell -a "bash ${make_dirt}/make.sh" -B 200 -P 5
}

###unarchive_module###
function start_module()
{
    local package_config=$1
    local start_path=$2
    ansible ${package_config} -m shell -a "bash ${start_path}/start.sh"
}

###stop_module###
function stop_module()
{
    local package_config=$1
    local stop_path=$2
    ansible ${package_config} -m shell -a "bash ${stop_path}/stop.sh"
}

###mkdir_module###
function mkdir_module()
{
    echo "this mkdir"
    local param1=$1
    local param2=$2
    ansible ${param1} -m shell -a "mkdir -p ${param2}"
}
###check_module###
function check_module()
{
    echo "this check"
    local package_config=$1
    local check_path=$2
    ansible ${param1} -m shell -a "bash  ${check_path}/check.sh"
}

###this_test_module###
function print_ip()
{
    echo "this print"
    local param1=$1
    local param2=$2
    echo "print ip => " ${param1}
    echo "print dir =>" ${param2}
    ansible ${param1} -m shell -a "echo ${param2}"
}

case $1 in
    copy) copy_module $2 $3 $4;;
    unarchive) unarchive_module $2 $3 $4;;
    build) build_module $2 $3;;
    start) start_module $2 $3;;
    stop) stop_module $2 $3;;
    mkdir) mkdir_module $2 $3;;
    check) check_module $2 $3;;
    this) print_ip $2 $3;;
    
    *) echo "others case";;
esac