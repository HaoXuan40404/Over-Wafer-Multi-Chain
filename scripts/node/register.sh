 #echo "start node$index ... "
 
dirpath="$(cd "$(dirname "$0")" && pwd)"
cd $dirpath
 
index=$1

if [ -d node$index ] && [ -f node$index/data/node.json ];then
    bash web3sdk/bin/web3sdk NodeAction registerNode file:`pwd`/node$index/data/node.json
else
    echo "node$index/node.json is node exist."
fi