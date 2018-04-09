#!/usr/bin/bash
print_log()
{
	if [ $# -lt 2 ]; then
		return 1
	fi

	fmt=""
	if [ $# -ge 3 ];then
	    fmt=$3
	fi

	echo -e "\033[${fmt}m[$1]$2\033[0m" 2>&1
	return 0
}
print_info()
{
	if [ $# -ne 1 ]; then
		return 1
	fi
	print_log "info" "$1" "1"
}
# configure local repository
setup_local_repo()
{
    print_info "Setup local repositories :$1"
    mkdir -p /etc/yum.repos.d/bak
    mv /etc/yum.repos.d/*.repo /etc/yum.repos.d/bak
    cat <<EOF | sudo tee /etc/yum.repos.d/Local.repo
[Local]
name=local Yum
baseurl=file://$1
gpgcheck=0
enabled=1
EOF
    createrepo $1
}

unsetup_local_repo()
{
    print_info "Clean up local repositories ..."
    ret=$(yum clean metadata && yum clean headers && yum clean all)
    if [ $? -ne 0 ]; then
        print_err "Clean up local repositories failed! Caused by $ret"
        return 1
    fi
    mv /etc/yum.repos.d/bak/*.repo /etc/yum.repos.d/
    mv /etc/yum.repos.d/Local.repo /etc/yum.repos.d/bak
}

case "$1" in
setup)
    setup_local_repo $2
    ;;
unset)
    unsetup_local_repo
    ;;
*)
    print_info "Unknown case $1"
    exit 0
    ;;
esac




