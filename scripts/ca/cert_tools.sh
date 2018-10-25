#!/bin/bash

EXIT_CODE=-1

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
check_env

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

    if [  -f "ca.key" -o -f "ca.req" -o -f "ca.crt" ]; then
        echo "ca.key or ca.req or ca.crt file exists, please clean all old files!"
        exit $EXIT_CODE
    fi

    openssl genrsa -out ca.key 2048
    openssl req -new -x509 -days 3650 -subj "/CN=$name/O=fiscobcos/OU=chain" -key ca.key -out ca.crt

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

    openssl genrsa -out $agencydir/agency.key 2048
    openssl req -new -sha256 -subj "/CN=$name/O=fiscobcos/OU=agency" -key $agencydir/agency.key -config cert.cnf -out $agencydir/agency.csr
    openssl x509 -req -days 3650 -sha256 -CA ca.crt -CAkey ca.key -CAcreateserial\
        -in $agencydir/agency.csr -out $agencydir/agency.crt  -extensions v4_req -extfile cert.cnf
    
    cp ca.crt cert.cnf $agencydir/
    cp ca.crt $agencydir/ca-agency.crt
    more $agencydir/agency.crt | cat >>$agencydir/ca-agency.crt
    echo "build $name agency cert successful!"
}

gen_cert_secp256k1() {
    store_dir="$1"
    name="$2"
    openssl ecparam -out $store_dir/${name}.param -name secp256k1
    openssl genpkey -paramfile $store_dir/${name}.param -out $store_dir/${name}.key
    openssl pkey -in $store_dir/${name}.key -pubout -out $store_dir/${name}.pubkey
    openssl req -new -sha256 -subj "/CN=$store_dir/O=fiscobcos/OU=${name}" -key $store_dir/${name}.key -config cert.cnf -out $store_dir/${name}.csr
    openssl x509 -req -days 3650 -sha256 -in $store_dir/${name}.csr -CAkey agency.key -CA agency.crt\
        -force_pubkey $store_dir/${name}.pubkey -out $store_dir/${name}.crt -CAcreateserial -extensions v3_req -extfile cert.cnf
    openssl ec -in $store_dir/${name}.key -outform DER | tail -c +8 | head -c 32 | xxd -p -c 32 | cat >$store_dir/${name}.private
}

gen_node_cert() {
    if [ "" = "`openssl ecparam -list_curves 2>&1 | grep secp256k1`" ]; then
        echo "openssl don't support secp256k1, please upgrade openssl!"
        exit $EXIT_CODE
    fi

    agency="$2"
    node="$3"
    check_name agency "$agency"
    check_name node "$node"

    dir_must_exists "$agency"
    file_must_exists "$agency/agency.key"
    dir_must_not_exists "$agency/$node"

    cd $agency
    mkdir -p $node
   
    gen_cert_secp256k1 $node node
    #nodeid is pubkey
    openssl ec -in $node/node.key -text -noout | sed -n '7,11p' | tr -d ": \n" | awk '{print substr($0,3);}' | cat >$node/node.nodeid
    openssl x509 -serial -noout -in $node/node.crt | awk -F= '{print $2}' | cat >$node/node.serial
    cp ca.crt agency.crt $node

    cd $node
    nodeid=`cat node.nodeid | head`
    serial=`cat node.serial | head`
    
    cat >node.json <<EOF
{
 "id":"$nodeid",
 "name":"$node",
 "agency":"$agency",
 "caHash":"$serial"
}
EOF
	cat >node.ca <<EOF
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
    file_must_exists "$agency/agency.key"
    dir_must_not_exists "$agency/$sdk"

    cd  $agency
    mkdir -p $sdk
    
    gen_cert_secp256k1 $sdk sdk
    cp ca-agency.crt $sdk/ca.crt
    
    read_password
    openssl pkcs12 -export -name client -passout "pass:$mypass" -in $sdk/sdk.crt -inkey $sdk/sdk.key -out $sdk/keystore.p12
    keytool -importkeystore -srckeystore $sdk/keystore.p12 -srcstoretype pkcs12 -srcstorepass $mypass\
        -destkeystore $sdk/client.keystore -deststoretype jks -deststorepass $mypass -alias client 2>/dev/null 

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
