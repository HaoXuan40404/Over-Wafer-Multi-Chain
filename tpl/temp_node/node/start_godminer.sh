#!/bin/bash
    ulimit -c unlimited
    nohup ./build/fisco-bcos  --genesis ./build/node0/genesis.json  --config ./build/node0/config.json  --godminer ./build/node0/log/log 2>&1 &
