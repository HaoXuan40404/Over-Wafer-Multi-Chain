function is_fisco_gm()
{
    local fisco=$1
    VERSION=$(${fisco} --version 2>&1 | head -1 | awk '{print $3}')
    if [ -z "${VERSION}" ];then
        echo " found not fisco version, fisco is ${fisco}"; exit 1;
    fi
    # FISCO BCOS gm version not support
    if  echo "$VERSION" | egrep "gm" ; then
        return 0
    fi 

    return 1
}

function fisco_version()
{
    local fisco=$1
    VERSION=$(${fisco} --version 2>&1 | head -1 | awk '{print $3}' | awk -F. '{print $1$2}')
    if [ -z "${VERSION}" ];then
        echo " found not fisco version, fisco is ${fisco}"; exit 1;
    fi
    echo "${VERSION}"
}