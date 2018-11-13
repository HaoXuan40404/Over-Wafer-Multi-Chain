#!/bin/bash
dirpath="$(cd "$(dirname "$0")" && pwd)"
    cd $dirpath
    ./fisco-bcos --genesis ${dirpath}/genesis.json  --config ${dirpath}/config.json --export-genesis $1  > ${dirpath}/fisco-bcos.log 2>&1

    echo "export genesis path => $1"