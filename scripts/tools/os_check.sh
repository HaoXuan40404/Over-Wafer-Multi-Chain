#!/bin/bash
dirpath="$(cd "$(dirname "$0")" && pwd)"
cd $dirpath

# Check the version of the OS, now support version: CentOS 7.2+ 64bits, Ubuntu 16.04 64bits, Redhat 7.2+, Oracle Linux Server 7.4+

OS_CENTOS='centos'
OS_UBUNTU='ubuntu'
OS_REDHAT='redhat'
OS_ORACLE='oracle'

function alarm()
{
    { echo "ERROR - $1"; exit 1; }
}

function os_check() 
{
    local os_version=''
    # Check for 'uname' and abort if it is not available.
    uname -v > /dev/null 2>&1 || { alarm " cannot use 'uname' to identify the platform."; }

    case $(uname -s) in
    #------------------------------------------------------------------------------
    # Linux
    #------------------------------------------------------------------------------
    Linux)

        if [ ! -f "/etc/os-release" ];then
             alarm "Unkown Linux distro, file /etc/os-release not exist"
        fi
        DISTRO_NAME=$(. /etc/os-release; echo $NAME)

        case $DISTRO_NAME in
    #------------------------------------------------------------------------------
    # Ubuntu  # At least 16.04
    #------------------------------------------------------------------------------
            Ubuntu*)

                UBUNTU_VERSION=""
                type lsb_release >/dev/null 2>&1
                if [ $? -eq 0 ];then
                    UBUNTU_VERSION=$(lsb_release -r | awk '{print $2}')
                else
                    UBUNTU_VERSION=$(. /etc/os-release; echo $VERSION | awk '{print $1}')
                fi

                ver=$(echo "$UBUNTU_VERSION" | awk -F . '{print $1$2}')
                #Ubuntu 16.04 or Ubuntu 16.04+
                if [ $ver -ne 1604 ];then
                    alarm "Unsupported Ubuntu Version. 16.04 is required, now is $UBUNTU_VERSION"
                fi

                os_version=$OS_UBUNTU

                ;;
    #------------------------------------------------------------------------------
    # CentOS  # At least 7.2
    #------------------------------------------------------------------------------
            CentOS*)
                CENTOS_VERSION=""
                if [ -f /etc/centos-release ];then
                    CENTOS_VERSION=$(cat /etc/centos-release)
                elif [ -f /etc/redhat-release ];then
                    CENTOS_VERSION=$(cat /etc/redhat-release)
                elif [ -f /etc/system-release ];then
                    CENTOS_VERSION=$(cat /etc/system-release)
                fi

                if [ -z "$CENTOS_VERSION" ];then
                    alarm "Unable to determine CentOS Version."
                fi

                ver=$(echo "$CENTOS_VERSION" | awk '{print $4}' | awk -F . '{print $1$2}')
                # CentOS 7.2 or CentOS 7.2+
                if [ $ver -lt 72 ];then
                    alarm "Unsupported CentOS Version, At least 7.2 is required, now is $CENTOS_VERSION"
                fi

                os_version=$OS_CENTOS
                ;;
    #------------------------------------------------------------------------------
    # Red Hat Enterprise Linux Server
    #------------------------------------------------------------------------------
            Red*) 
                REDHAT_LINUX_VERSION=""
                 if [ -f /etc/redhat-release ];then
                    REDHAT_LINUX_VERSION=$(cat /etc/redhat-release)
                elif [ -f /etc/system-release ];then
                    REDHAT_LINUX_VERSION=$(cat /etc/system-release)
                fi

                if [ -z "$REDHAT_LINUX_VERSION" ];then
                    alarm "Unable to determine Red Hat Enterprise Linux Server."
                fi

                ver=$(echo "$REDHAT_LINUX_VERSION" | awk '{print $7}' | awk -F . '{print $1$2}')

                #Red Hat Enterprise Linux Server+
                if [ $ver -lt 74 ];then
                    alarm "Unsupported Red Hat Version, At least 7.4 Red Hat is required, now is $REDHAT_LINUX_VERSION"
                fi

                os_version=$OS_REDHAT

                ;;           
    #------------------------------------------------------------------------------
    # Oracle Linux Server # At least 7.4
    #------------------------------------------------------------------------------
            Oracle*) 
                ORACLE_LINUX_VERSION=""
                if [ -f /etc/oracle-release ];then
                    ORACLE_LINUX_VERSION=$(cat /etc/oracle-release)
                elif [ -f /etc/system-release ];then
                    ORACLE_LINUX_VERSION=$(cat /etc/system-release)
                fi

                if [ -z "$ORACLE_LINUX_VERSION" ];then
                    alarm "Unable to determine Oracle Linux version."
                fi

                ver=$(echo "$ORACLE_LINUX_VERSION" | awk '{print $5}' | awk -F . '{print $1$2}')
                #Oracle Linux 7.4 or Oracle Linux 7.4+
                if [ $ver -lt 74 ];then
                    alarm "Unsupported Oracle Linux, At least 7.4 is required, now is $ORACLE_LINUX_VERSION"
                fi

                os_version=$OS_ORACLE

                ;;
    #------------------------------------------------------------------------------
    # Other Linux
    #------------------------------------------------------------------------------
            *)
                alarm "Unsupported Linux distribution: $DISTRO_NAME."
                ;;
        esac # case $DISTRO_NAME

        ;; #Linux)

    #------------------------------------------------------------------------------
    # Other platform (not Linux, FreeBSD or macOS).
    #------------------------------------------------------------------------------
    *)
        #other
        alarm "Unsupported or Unidentified OS."
        ;;
    esac

    echo ${os_version}
}

