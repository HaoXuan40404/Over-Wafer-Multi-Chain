#!/bin/bash

store_path=$1
agency=$2

openssl ec -in $store_path/node.key -outform DER | tail -c +8 | head -c 32 | xxd -p -c 32 | cat >$store_path/node.private

openssl ec -in $store_path/node.key -text -noout | sed -n '7,11p' | tr -d ": \n" | awk '{print substr($0,3);}' | cat >$store_path/node.nodeid
openssl x509 -serial -noout -in $store_path/node.crt | awk -F= '{print $2}' | cat >$store_path/node.serial
#cp ca.crt agency.crt $node
nodeid=`cat $store_path/node.nodeid | head`
serial=`cat $store_path/node.serial | head`
    
cat >$store_path/node.json <<EOF
{
 "id":"$nodeid",
 "name":"$node",
 "agency":"$agency",
 "caHash":"$serial"
}
EOF
cat >$store_path/node.ca <<EOF
{
 "serial":"$serial",
 "pubkey":"$nodeid",
 "name":"$node"
}
EOF

echo "build node cert successful!"