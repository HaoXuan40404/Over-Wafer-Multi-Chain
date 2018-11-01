#!/bin/bash

OPENSSL_CMD={GM_PATH}
EXIT_CODE=-1

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
"usage command gen_chain_cert chainname|
              gen_agency_cert agencyname|
              gen_node_cert agencyname nodename|
              gen_sdk_cert agencyname sdkname|
              help"
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
    name="$2"
    check_name chain "$name"
    if [ -f "gmca.key" -o -f "gmca.crt" ]; then
        echo "gmca.key or gmca.crt file exists, please clean all old files!"
        exit $EXIT_CODE
    fi

	$OPENSSL_CMD genpkey -paramfile gmsm2.param -out gmca.key
	$OPENSSL_CMD req -config cert.cnf -x509 -days 3650 -subj "/CN=$name/O=fiscobcos/OU=chain" -key gmca.key -extensions v3_ca -out gmca.crt

    if [ $? -eq 0 ]; then
        echo "build chain ca succussful!"
    else
        echo "please input at least Common Name!"
    fi
}

gen_agency_cert() {
    name="$2"
    check_name agency "$name"
    dir_must_not_exists "$name"

    mkdir $name
    agencydir=$name

    $OPENSSL_CMD genpkey -paramfile gmsm2.param -out $agencydir/gmagency.key
    $OPENSSL_CMD req -new -subj "/CN=$name/O=fiscobcos/OU=agency" -key $agencydir/gmagency.key -config cert.cnf -out $agencydir/gmagency.csr
    $OPENSSL_CMD x509 -req -days 3650 -CA gmca.crt -CAkey gmca.key -CAcreateserial\
        -in $agencydir/gmagency.csr -out $agencydir/gmagency.crt -extfile cert.cnf -extensions v3_agency_root

    cp gmca.crt cert.cnf gmsm2.param $agencydir/
    rm -rf $agencydir/*.csr
    echo "build $name agency cert successful!"
}

gen_node_cert() {
    agency="$2"
    node="$3"
    check_name agency "$agency"
    check_name node "$node"

    dir_must_exists "$agency"
    file_must_exists "$agency/gmagency.key"
    dir_must_not_exists "$agency/$node"
    
    cd $agency
    mkdir -p $node
    
    echo "gen signature certificate with guomi algorithm:"
    $OPENSSL_CMD genpkey -paramfile gmsm2.param -out $node/gmnode.key
    $OPENSSL_CMD req -new -key $node/gmnode.key -subj "/CN=$node/O=fiscobcos/OU=node" -config cert.cnf -out $node/gmnode.csr
    $OPENSSL_CMD x509 -req -CA gmagency.crt -CAkey gmagency.key -days 3650 -CAcreateserial\
        -in $node/gmnode.csr -out $node/gmnode.crt -extfile cert.cnf -extensions v3_req
    
    echo "gen encryption certificate with guomi algorithm:"
    $OPENSSL_CMD genpkey -paramfile gmsm2.param -out $node/gmennode.key
    $OPENSSL_CMD req -new -key $node/gmennode.key -subj "/CN=$node/O=fiscobcos/OU=ennode" -config cert.cnf -out $node/gmennode.csr
    $OPENSSL_CMD x509 -req -CA gmagency.crt -CAkey gmagency.key -days 3650 -CAcreateserial\
        -in $node/gmennode.csr -out $node/gmennode.crt -extfile cert.cnf -extensions v3enc_req
    
    $OPENSSL_CMD ec -in $node/gmnode.key -outform DER | tail -c +8 | head -c 32 | xxd -p -c 32 | cat >$node/gmnode.private
    #nodeid is pubkey
    $OPENSSL_CMD ec -in $node/gmnode.key -text -noout | sed -n '7,11p' | tr -d ": \n" | awk '{print substr($0,3);}' | cat >$node/gmnode.nodeid
    openssl x509 -serial -noout -in $node/gmnode.crt | awk -F= '{print $2}' | cat >$node/gmnode.serial
    cp gmca.crt gmagency.crt $node
    rm -rf $node/*.csr

    cd $node
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

    agency="$2"
    sdk="$3"
    check_name agency "$agency"
    check_name sdk "$sdk"

    dir_must_exists "$agency"
    dir_must_not_exists "$agency/$sdk"

    cd  $agency
    mkdir -p $sdk
   
    cat >RSA.cnf <<EOF
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
    openssl genrsa -out $sdk/ca.key 2048
    openssl req -config cert.cnf -new -x509 -days 3650 -subj "/CN=$sdk/O=fiscobcos/OU=gmsdkca" -key $sdk/ca.key -out $sdk/ca.crt
    #gen sdk cert
    openssl genrsa -out $sdk/server.key 2048
    openssl req -new -subj "/CN=$sdk/O=fiscobcos/OU=gmsdk" -key $sdk/server.key -config cert.cnf -out $sdk/server.csr
    openssl x509 -req -days 3650 -CA $sdk/ca.crt -CAkey $sdk/ca.key -CAcreateserial\
        -in $sdk/server.csr -out $sdk/server.crt -extensions v3_req -extfile RSA.cnf
    
    #read_password
    mypass=123456
    openssl pkcs12 -export -name client -passout "pass:$mypass" -in $sdk/server.crt -inkey $sdk/server.key -out $sdk/keystore.p12
    keytool -importkeystore -srckeystore $sdk/keystore.p12 -srcstoretype pkcs12 -srcstorepass $mypass\
        -destkeystore $sdk/client.keystore -deststoretype jks -deststorepass $mypass -alias client 2>/dev/null 
    rm -rf $sdk/*.{srl,csr}
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
