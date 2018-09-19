#!/bin/bash
installPWD=$PWD
echo $PWD
source $PWD/dependencies_check.sh
source $PWD/dependencies_install.sh
source $PWD/os_version_check.sh
#check sudo permission
request_sudo_permission
# operation system check
os_version_check
#dependencies check
dependencies_install
dependencies_check
