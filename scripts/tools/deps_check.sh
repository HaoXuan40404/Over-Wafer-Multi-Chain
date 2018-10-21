#!/bin/bash
source ~/.bash_profile
source /etc/profile
#check if $1 is install
function check_if_install()
{
    type $1 >/dev/null 2>&1
    if [ $? -ne 0 ];then
        { echo "ERROR - $1 is not installed."; }
    else
        echo "$1 is installed.";
    fi
}

#Oracle JDK 1.8 be requied.
function java_version_check()
{
    check_if_install java

    check_if_install keytool

    #JAVA version
    JAVA_VER=$(java -version 2>&1 | sed -n ';s/.* version "\(.*\)\.\(.*\)\..*".*/\1\2/p;')
   
    if [ -z "$JAVA_VER" ];then
        { echo "ERROR - failed to get java version, version is `java -version 2>&1 | grep java`."; exit 1; }
    fi    

    #Oracle JDK 1.8
    if [ $JAVA_VER -eq 18 ] && [[ $(java -version 2>&1 ) ]];then
        #is java and keytool match ?
        JAVA_PATH=$(dirname `which java`)
        KEYTOOL_PATH=$(dirname `which keytool`)
        if [ "$JAVA_PATH" = "$KEYTOOL_PATH" ];then
            echo " java path => "${JAVA_PATH}
            echo " keytool path => "${KEYTOOL_PATH}
            return
        fi

        { echo "Oracle JDK 1.8 be requied, now JDK is `java -version 2>&1 | grep java`"; }
    fi
    
    { echo "Oracle JDK 1.8 be requied, now JDK is `java -version 2>&1 | grep java`"; }
} 

#openssl 1.0.2 be requied.
function openssl_version_check()
{
    check_if_install openssl

    #openssl version
    OPENSSL_VER=$(openssl version 2>&1 | sed -n ';s/.*OpenSSL \(.*\)\.\(.*\)\.\([0-9]*\).*/\1\2\3/p;')

    if [ -z "$OPENSSL_VER" ];then
        { echo  "failed to get openssl version, version is `openssl version`" ; }
    fi

    #openssl 1.0.2
    if [ $OPENSSL_VER -eq 102 ];then
        return 
    fi

    { echo "OpenSSL 1.0.2 be requied , now OpenSSL version is `openssl version`" ; }
}

# version check
function deps_check()
{
    # java => Oracle JDK 1.8
    java_version_check
    # openssl => OpenSSL 1.0.2
    openssl_version_check

    # lsof
    check_if_install lsof
    # envsubst
    check_if_install envsubst
    # xxd
    check_if_install xxd
    # bc
    check_if_install bc

    # add more check here
}

deps_check