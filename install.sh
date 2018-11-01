#!/bin/bash
# OWMC init and install shell.
set -x

dirpath="$(cd "$(dirname "$0")" && pwd)"
cd $dirpath

function alarm()
{
    echo "\033[1;31m $1 \033[0m"; exit 1;
}

function check_file()
{
    local file=$1
    if [ -z $file ];then
        alarm " not found file $file."
    fi
}

function check_install()
{
    type $1 >/dev/null 2>&1
    [ $1 -ne 0 ] && {
        alarm " $1 is not installed."
    }
}

function sudo_permission_check() 
{
    sudo echo -n " "

    if [ $? -ne 0 ]; then
        alarm "no sudo permission, please add youself in the sudoers"
    fi
}

function format()
{
	find . -name "*.json"|  while read LINE; do  dos2unix $LINE  2>/dev/null ; done
    find . -name "*.sh"|  while read LINE; do chmod +x $LINE; dos2unix $LINE 2>/dev/null ; done
    find . -name "web3sdk"|  while read LINE; do chmod +x $LINE; dos2unix $LINE 2>/dev/null ; done
}

DEFAULT_INSTALL_DIR='/usr/local/'
DEFAULT_PYTHON_ENV='/usr/bin/python'
function OWMC_install()
{
    local install_dir=$1
    if [ -z "${install_dir}" ];then
        install_dir=${DEFAULT_INSTALL_DIR}
    fi

    local python_env=${DEFAULT_PYTHON_ENV}
    echo " OWMC install dictionary is ${install_dir}"
    echo " OWMC python env is ${python_env}"

    if [ -d ${install_dir}/OWMC ];then
        alarm " ${install_dir} already exist, OWMC maybe has been installed, --force can be set to install again. "
    fi

    sudo mkdir ${install_dir}/OWMC
    sudo cp $dirpath/*  ${install_dir}/OWMC/

}

function deps_install()
{

}

function deps_check()
{
    check_install dos2unix 
    check_install envsubst
}

function main()
{
    #
    sudo_permission_check
    # dos2unix to json and sh file
    format
    # install all OWMC deps soft
    deps_install
    # check if OWMC deps soft install success
    deps_check
    # 
    OWMC_install
}