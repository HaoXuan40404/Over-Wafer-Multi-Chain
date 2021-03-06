#!/bin/bash
dirpath="$(cd "$(dirname "$0")" && pwd)"
cd $dirpath

cert_conf_path=$dirpath/cert.cnf

OPENSSL_CMD={GM_PATH}
EXIT_CODE=-1

mypass=123456

check_openssl_gm() {
    if [ ! -f "$OPENSSL_CMD" ]; then
        echo "please install openssl guomi version or change OPENSSL_CMD variable!"
        exit $EXIT_CODE
    fi
    if [ "" = "`$OPENSSL_CMD ecparam -list_curves | grep SM2`" ]; then
        echo "current openssl does not support SM2, please upgrade tassl!"
        exit $EXIT_CODE
    fi
}
check_openssl_gm

check_env() {
    version=`openssl version 2>&1 | grep 1.0.2`
    [ -z "$version" ] && {
        echo "please install openssl 1.0.2k-fips!"
        #echo "please install openssl 1.0.2 series!"
        #echo "download openssl from https://www.openssl.org."
        echo "use \"openssl version\" command to check."
        exit $EXIT_CODE
    }
}
#check_env

check_java() {
    ver=`java -version 2>&1 | grep version | grep 1.8`
    tm=`java -version 2>&1 | grep "Java(TM)"`
    [ -z "$ver" -o -z "$tm" ] && {
        echo "please install java Java(TM) 1.8 series!"
        echo "use \"java -version\" command to check."
        exit $EXIT_CODE
    }

    which keytool >/dev/null 2>&1
    [ $? != 0 ] && {
        echo "keytool command not exists!"
        exit $EXIT_CODE
    }
}

usage() {
printf "%s\n" \
"usage command gen_chain_cert chaindir|
              gen_agency_cert chaindir agencydir|
              gen_node_cert agencydir nodedir|
              gen_sdk_cert agencydir sdkdir|
              help"
}

getname() {
    local name="$1"
    if [ -z "$name" ]; then
        return 0
    fi
    [[ "$name" =~ ^.*/$ ]] && {
        name="${name%/*}"
    }
    name="${name##*/}"
    echo "$name"
}

check_name() {
    local name="$1"
    local value="$2"
    [[ "$value" =~ ^[a-zA-Z0-9._-]+$ ]] || {
        echo "$name name [$value] invalid, it should match regex: ^[a-zA-Z0-9._-]+\$"
        exit $EXIT_CODE
    }
}

file_must_exists() {
    if [ ! -f "$1" ]; then
        echo "$1 file does not exist, please check!"
        exit $EXIT_CODE
    fi
}

dir_must_exists() {
    if [ ! -d "$1" ]; then
        echo "$1 DIR does not exist, please check!"
        exit $EXIT_CODE
    fi
}

dir_must_not_exists() {
    if [  -d "$1" ]; then
        echo "$1 DIR exists, please clean old DIR!"
        exit $EXIT_CODE
    fi
}


gen_chain_cert() {
    path="$2"
    name=12345
    chaindir=$path
    if [ ! -d $path ]; then
        mkdir -p $chaindir
    fi

	$OPENSSL_CMD genpkey -paramfile gmsm2.param -out $chaindir/gmca.key
	$OPENSSL_CMD req -config ${cert_conf_path} -x509 -days 3650 -subj "/CN=$name/O=fiscobcos/OU=chain" -key $chaindir/gmca.key -extensions v3_ca -out $chaindir/gmca.crt
    cp gmsm2.param $chaindir

    if [ $? -eq 0 ]; then
        echo "build chain ca succussful!"
    else
        echo "please input at least Common Name!"
    fi
}

gen_agency_cert() {
    chain="$2"
    agencypath="$3"
    name="$4"

    dir_must_exists "$chain"
    file_must_exists "$chain/gmca.key"
    check_name agency "$name"
    agencydir=$agencypath'/'$name
    dir_must_not_exists "$agencydir"
    mkdir -p $agencydir

    $OPENSSL_CMD genpkey -paramfile $chain/gmsm2.param -out $agencydir/gmagency.key
    $OPENSSL_CMD req -new -subj "/CN=$name/O=fiscobcos/OU=agency" -key $agencydir/gmagency.key -config ${cert_conf_path} -out $agencydir/gmagency.csr
    $OPENSSL_CMD x509 -req -days 3650 -CA $chain/gmca.crt -CAkey $chain/gmca.key -CAcreateserial\
        -in $agencydir/gmagency.csr -out $agencydir/gmagency.crt -extfile ${cert_conf_path} -extensions v3_agency_root

    cp $chain/gmca.crt $chain/gmsm2.param $agencydir/
    rm -rf $agencydir/*.csr
    echo "build $name agency cert successful!"
}

gen_node_cert() {
    agpath="$2"
    agency=`getname "$agpath"`
    nodepath="$3"
    node="$4"
    ndpath=$nodepath
    dir_must_exists "$agpath"
    file_must_exists "$agpath/gmagency.key"
    check_name agency "$agency"
    check_name node "$node"
    if [ ! -d $ndpath ]; then
        mkdir -p $ndpath
    fi
    
    echo "gen signature certificate with guomi algorithm:"
    $OPENSSL_CMD genpkey -paramfile $agpath/gmsm2.param -out $ndpath/gmnode.key
    $OPENSSL_CMD req -new -key $ndpath/gmnode.key -subj "/CN=$node/O=fiscobcos/OU=node" -config ${cert_conf_path} -out $ndpath/gmnode.csr
    $OPENSSL_CMD x509 -req -CA $agpath/gmagency.crt -CAkey $agpath/gmagency.key -days 3650 -CAcreateserial\
        -in $ndpath/gmnode.csr -out $ndpath/gmnode.crt -extfile ${cert_conf_path} -extensions v3_req
    
    echo "gen encryption certificate with guomi algorithm:"
    $OPENSSL_CMD genpkey -paramfile $agpath/gmsm2.param -out $ndpath/gmennode.key
    $OPENSSL_CMD req -new -key $ndpath/gmennode.key -subj "/CN=$node/O=fiscobcos/OU=ennode" -config ${cert_conf_path} -out $ndpath/gmennode.csr
    $OPENSSL_CMD x509 -req -CA $agpath/gmagency.crt -CAkey $agpath/gmagency.key -days 3650 -CAcreateserial\
        -in $ndpath/gmennode.csr -out $ndpath/gmennode.crt -extfile ${cert_conf_path} -extensions v3enc_req
    
    $OPENSSL_CMD ec -in $ndpath/gmnode.key -outform DER | tail -c +8 | head -c 32 | xxd -p -c 32 | cat >$ndpath/gmnode.private
    #nodeid is pubkey
    $OPENSSL_CMD ec -in $ndpath/gmnode.key -text -noout | sed -n '7,11p' | tr -d ": \n" | awk '{print substr($0,3);}' | cat >$ndpath/gmnode.nodeid
    openssl x509 -serial -noout -in $ndpath/gmnode.crt | awk -F= '{print $2}' | cat >$ndpath/gmnode.serial
    cp $agpath/gmca.crt $agpath/gmagency.crt $ndpath
    rm -rf $ndpath/*.csr

    cd $ndpath
    nodeid=`cat gmnode.nodeid | head`
    serial=`cat gmnode.serial | head`
    
    cat >gmnode.json <<EOF
{
 "id":"$nodeid",
 "name":"$node",
 "agency":"$agency",
 "caHash":"$serial"
}
EOF
	cat >gmnode.ca <<EOF
{
 "serial":"$serial",
 "pubkey":"$nodeid",
 "name":"$node"
}
EOF

    echo "build $node node cert successful!"
}

read_password() {
    read -se -p "Enter password for keystore:" pass1
    echo
    read -se -p "Verify password for keystore:" pass2
    echo
    [[ "$pass1" =~ ^[a-zA-Z0-9._-]{6,}$ ]] || {
        echo "password invalid, at least 6 digits, should match regex: ^[a-zA-Z0-9._-]{6,}\$"
        exit $EXIT_CODE
    }
    [ "$pass1" != "$pass2" ] && {
        echo "Verify password failure!"
        exit $EXIT_CODE
    }
    mypass=$pass1
}

gen_sdk_cert() {
    check_java

    agpath="$2"
    agency=`getname "$agpath"`
    sdkph="$3"
    sdk="sdk"
    dir_must_exists "$agpath"
    file_must_exists "$agpath/gmagency.key"
    check_name agency "$agency"
    sdkpath=$sdkph'/'$sdk
    dir_must_not_exists "$sdkpath"
    mkdir -p $sdkpath
    
    cat >$sdkpath/RSA.cnf <<EOF
[ca]
default_ca=default_ca
[default_ca]
default_md = sha256
[req]
distinguished_name = req_distinguished_name
req_extensions = v3_req
[req_distinguished_name]
countryName = CN
countryName_default = CN
stateOrProvinceName = State or Province Name (full name)
stateOrProvinceName_default =GuangDong
localityName = Locality Name (eg, city)
localityName_default = ShenZhen
organizationalUnitName = Organizational Unit Name (eg, section)
organizationalUnitName_default = fiscobcos
commonName =  Organizational  commonName (eg, fiscobcos)
commonName_default = fiscobcos
commonName_max = 64
[ v3_req ]
# Extensions to add to a certificate request
basicConstraints = CA:FALSE
keyUsage = nonRepudiation, digitalSignature, keyEncipherment
EOF

    #gen ca cert
    openssl genrsa -out $sdkpath/ca.key 2048
    openssl req -config ${cert_conf_path} -new -x509 -days 3650 -subj "/CN=$sdk/O=fiscobcos/OU=gmsdkca" -key $sdkpath/ca.key -out $sdkpath/ca.crt
    #gen sdk cert
    openssl genrsa -out $sdkpath/server.key 2048
    openssl req -new -subj "/CN=$sdk/O=fiscobcos/OU=gmsdk" -key $sdkpath/server.key -config ${cert_conf_path} -out $sdkpath/server.csr
    openssl x509 -req -days 3650 -CA $sdkpath/ca.crt -CAkey $sdkpath/ca.key -CAcreateserial\
        -in $sdkpath/server.csr -out $sdkpath/server.crt -extensions v3_req -extfile $sdkpath/RSA.cnf
    
    
    openssl pkcs12 -export -name client -passout "pass:$mypass" -in $sdkpath/server.crt -inkey $sdkpath/server.key -out $sdkpath/keystore.p12
    keytool -importkeystore -srckeystore $sdkpath/keystore.p12 -srcstoretype pkcs12 -srcstorepass $mypass\
        -destkeystore $sdkpath/client.keystore -deststoretype jks -deststorepass $mypass -alias client 2>/dev/null 
    rm -rf $sdkpath/*.{srl,csr}
    echo "build $sdk sdk cert successful!"
}

case "$1" in
gen_chain_cert)
    gen_chain_cert "$1" "$2" "$3" "$4" "$5" "$6" "$7" "$8" "$9"
    ;;
gen_agency_cert)
    gen_agency_cert "$1" "$2" "$3" "$4" "$5" "$6" "$7" "$8" "$9"
    ;;
gen_node_cert)
    gen_node_cert "$1" "$2" "$3" "$4" "$5" "$6" "$7" "$8" "$9"
    ;;
gen_sdk_cert)
    gen_sdk_cert "$1" "$2" "$3" "$4" "$5" "$6" "$7" "$8" "$9"
    ;;
help)
    usage
    ;;
*)
    usage
esac
