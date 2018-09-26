#!/bin/bash

# check user has sudo permission
function request_sudo_permission() 
{
    sudo echo -n " "

    if [ $? -ne 0 ]; then
        { echo "ERROR - no sudo permission, please add youself in the sudoers."; exit 1; }
    fi
}

function deps_install() 
{
    # sudo permission check
    request_sudo_permission
	
    # Check for 'uname' and abort if it is not available.
    uname -v > /dev/null 2>&1 || { echo "ERROR - use 'uname' to identify the platform."; exit 1; }

    case $(uname -s) in 

    #------------------------------------------------------------------------------
    # Linux
    #------------------------------------------------------------------------------
    Linux)

        if [ ! -f "/etc/os-release" ];then
            { echo "ERROR - Unsupported or unidentified Linux distro."; exit 1; }
        fi

        DISTRO_NAME=$(. /etc/os-release; echo $NAME)
        # echo "Linux distribution: $DISTRO_NAME."

        case $DISTRO_NAME in
    #------------------------------------------------------------------------------
    # Ubuntu 16.04
    #------------------------------------------------------------------------------
            Ubuntu*)

                    sudo apt-get -y install lsof
                    sudo apt-get -y install gettext
                    sudo apt-get -y install bc
                    sudo apt-get -y install openssl
                    sudo apt-get -y install build-essential
                    sudo apt-get -y install libcurl4-openssl-dev libgmp-dev
                    sudo apt-get -y install libleveldb-dev  libmicrohttpd-dev
                    sudo apt-get -y install libminiupnpc-dev
                    sudo apt-get -y install libssl-dev libkrb5-dev
                    sudo apt-get -y install uuid-dev
                    sudo apt-get -y install vim-common

                ;;
    #------------------------------------------------------------------------------
    # CentOS  # At least 7.2
    #------------------------------------------------------------------------------
            CentOS*)

                    sudo yum -y install bc
                    sudo yum -y install gettext
                    sudo yum -y install openssl openssl-devel
                    sudo yum -y install leveldb-devel curl-devel 
                    sudo yum -y install libmicrohttpd-devel gmp-devel 
                    sudo yum -y install lsof
                    sudo yum -y install libuuid-devel
                    sudo yum -y install  vim-common

                ;;
    #------------------------------------------------------------------------------
    # Oracle Linux Server # At least 7.4
    #------------------------------------------------------------------------------
            Oracle*) 
                   
                    sudo yum -y install lsof
                    sudo yum -y install bc
                    sudo yum -y install gettext
                    sudo yum -y install openssl openssl-devel
                    sudo yum -y install leveldb-devel curl-devel 
                    sudo yum -y install libmicrohttpd-devel gmp-devel 
                    sudo yum -y install libuuid-devel

                ;;
    #------------------------------------------------------------------------------
    # Other Linux
    #------------------------------------------------------------------------------
            *)
                { echo "ERROR - Unsupported Linux distribution: $DISTRO_NAME."; exit 1; }
                ;;
        esac # case $DISTRO_NAME

        ;; #Linux)

    #------------------------------------------------------------------------------
    # Other platform (not Linux, FreeBSD or macOS).
    #------------------------------------------------------------------------------
    *)
        #other
        { echo "ERROR - Unsupported or unidentified OS."; exit 1; }
        ;;
    esac
}

deps_install
