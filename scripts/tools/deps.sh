
#!/bin/bash
dirpath="$(cd "$(dirname "$0")" && pwd)"
cd $dirpath

source $dirpath/os_check.sh

REDHAT_DEPS="nmap openssl openssl-devel leveldb-devel libcurl-devel libmicrohttpd-devel gmp-devel libuuid-devel"
UBUNTU_DEPS="nmap openssl build-essential libcurl4-openssl-dev libgmp-dev libleveldb-dev  libmicrohttpd-dev libminiupnpc-dev libssl-dev libkrb5-dev uuid-dev"

#check if $1 is install
function check_install()
{
    type $1 >/dev/null 2>&1
    if [ $? -ne 0 ];then
        return 1
    fi

    return 0
}

function yum_is_install()
{
    if yum list installed "$1" >/dev/null 2>&1; then
        return 0
    else
        return 1
    fi
}

function apt_is_install()
{
    if sudo dpkg -s $1 | egrep -i Status >/dev/null 2>&1; then
        return 0
    else
        return 1
    fi
}

function deps_install() 
{
    # sudo permission check
    sudo echo -n " "
    if [ $? -ne 0 ]; then
        { echo " ERROR - no sudo permission, please add youself in the sudoers."; exit 1; }
    fi

    # os_check
    os_version=$(os_check)

    case ${os_version} in
    $OS_CENTOS|$OS_REDHAT|$OS_ORACLE)
        sudo yum -y install ${REDHAT_DEPS} >/dev/null 2>&1
        # for dep in ${REDHAT_DEPS}
        # do
        #     sudo yum -y install ${dep} >/dev/null 2>&1
        # done
    ;;
    $OS_UBUNTU)
        sudo apt-get install ${UBUNTU_DEPS} >/dev/null 2>&1
        # for dep in ${UBUNTU_DEPS}
        # do
        #     sudo apt-get install ${dep} >/dev/null 2>&1
        # done
    ;;
    esac
}

function deps_check()
{
     # sudo permission check
    sudo echo -n " "
    if [ $? -ne 0 ]; then
        { echo " ERROR - no sudo permission, please add youself in the sudoers."; exit 1; }
    fi

    # os_check
    os_version=$(os_check)
    deps=''
    case ${os_version} in
    $OS_CENTOS|$OS_REDHAT|$OS_ORACLE)
        for i in ${REDHAT_DEPS}
        do
            if $(yum_is_install $i);then
                echo " $i is installed."
            else
                echo " $i is not installed."
            fi
        done
    ;;
    $OS_UBUNTU)
        for i in ${UBUNTU_DEPS}
        do
            if $(apt_is_install $i);then
                echo " $i is installed."
            else
                echo " $i is not installed."
            fi
        done
    ;;
    esac

    openssl_check
    java_check
}

#openssl 1.0.2 be requied.
function openssl_check()
{
    if $(check_install openssl);then
       echo " " 
    else
        echo " ERROR - openssl is not installed." ; exit 1;
    fi

    #openssl version
    OPENSSL_VER=$(openssl version 2>&1 | sed -n ';s/.*OpenSSL \(.*\)\.\(.*\)\.\([0-9]*\).*/\1\2\3/p;')
    if [ -z "$OPENSSL_VER" ];then
        { echo  " ERROR - openssl unkown version, now is `openssl version`" ; exit 1 ; }
    fi

    #openssl 1.0.2
    if [ $OPENSSL_VER -ne 102 ];then
        { echo " ERROR - OpenSSL 1.0.2 be requied , now is `openssl version`" ; } 
    fi

    echo " openssl version is ${OPENSSL_VER}. "
}

#Oracle JDK 1.8 be requied.
function java_check()
{
    if $(check_install java);then
       echo "" 
    else
        echo " java is not installed." ; exit 1;
    fi

    #JAVA version
    JAVA_VER=$(java -version 2>&1 | head -n 1 | awk -F '"' '{print $2}' | awk -F . '{print $1$2}')
    if [ -z "$JAVA_VER" ];then
        { echo "ERROR -  java unkown version, now is `java -version 2>&1 | head -n 1 | awk -F '"' '{print $2}'`."; exit 1; }
    fi 

    if  java -version 2>&1 | egrep -i openjdk >/dev/null 2>&1;then
    #openjdk
        if [ ${JAVA_VER} -le 18 ];then
            { echo "ERROR -  OpenJDK need 1.9 or above, now is ${JAVA_VER}. "; exit 1; } 
        fi
    else
        if [ ${JAVA_VER} -lt 18 ];then
            { echo "ERROR -  OracleJDK need 1.8 or above, now is ${JAVA_VER}. "; exit 1; } 
        fi
    fi 

    echo " java version is ${JAVA_VER}. "
} 