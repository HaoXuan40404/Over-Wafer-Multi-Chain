#!/bin/bash
# OWMC init and install shell.

set -e

dirpath="$(cd "$(dirname "$0")" && pwd)"
cd $dirpath

function alarm()
{
    local content=${1}
    echo -e "\033[31m ${content} \033[0m"
}

# check python enviroment.
function check_python()
{
    python=$1
    py_version=$($python -V 2>/dev/null | awk {'print $2'} | awk -F. {' print $1"."$2"."$3 '}
3.6.6)
    if [ ! -z '${py_version}' ];then
        # echo " python path is ${python}, version is ${py_version}"
        return 0
    fi
    return 1
}

# check if soft installed.
function check_install()
{
    type $1 >/dev/null 2>&1
    [ $1 -ne 0 ] && {
        alarm " $1 is not installed."
    }
}

# check sudo permission
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

function deps_install()
{

}

function deps_check()
{

}

#OWMC install dir, default '/usr/local/'
install_dir="/usr/local/"
python_env='/usr/bin/python'
force="false"
gm="false"
OWMC="/usr/bin/OWMC"
function install()
{
    # sudo permission check
    sudo_permission_check
    
    # params check
    if ! $(check_python);then
        alarm " Not invalid python path."; exit 1;
    fi

    if [ -f $OWMC ];then
        if force == "true";then
            sudo rm -rf $OWMC
        else
            alarm " $OWMC already install, set '-f' to force install." ; exit 1;
        fi
    fi

    if [ -d ${install_dir}/OWMC ];then
        if force == "true";then
            sudo rm -rf ${install_dir}/OWMC
        else
            alarm " $OWMC already install, set '-f' to force install." ; exit 1;
        fi
    fi

    echo " OWMC install dir is ${install_dir}"
    echo " OWMC python env is ${python_env}"

    sudo mkdir -p ${install_dir}/OWMC
    sudo cp $dirpath/*  ${install_dir}/OWMC/

    deps_install
}

function help() 
{
    echo "Usage:"
    echo "Optional:"
    echo "    -d  <dir>           The dir of OWMC will be install. (default: /usr/loca/)"
    echo "    -p  <path>          The python path. (default: /usr/bin/python) "
    echo "    -g 			      Install guomi deps. (default: not install guomi deps.)"
    echo "    -f                  Install OWMC even if it has been installed."
    echo "    -h                  This help"
    echo "Example:"
    echo "    bash install.sh "
    echo "    bash install.sh -d /usr/local -p /usr/bin/python -f -g "
    exit 0
}

function main()
{
    while getopts "d:p:gfh" option;do
        case $option in
        d) install_dir=$OPTARG;;
        p) python_env=$OPTARG;;
        f) force="true"
        g) gm="true"
        h) help;;
        esac
    done

    # install
    install
}

main