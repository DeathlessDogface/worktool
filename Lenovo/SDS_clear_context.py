#!/usr/bin/python
import os

def remove_package(name):
    cmds=[]
    with os.popen("rpm -qa|grep %s"%name) as p_name:
        while True:
            try:
                cmds.append("rpm -e --nodeps %s"%p_name.next())
            except StopIteration:
                break
    return cmds

def main():
    cmd_list=[]
    for pkg in [
        "storagemgmt-client",
        "storagemgmt-api",
        "openstack-keystone",
        "python-keystoneclient",
        "python-django-horizon",
        "openstack-dashboard",
        "openstack-keystone",
        "python-django-openstack-auth",
        "rabbitmq-server",
        "sds-agent",
        "mariadb"
    ]:
        cmd_list.extend(remove_package(pkg))
    cmd_list.extend(["umount /dev/sd%s"% i for i in list("abcdefghijkl")])
    cmd_list.append("/etc/ceph/scripts/disk_fs_mgmt.sh -O deletepartition")
    cmd_list.append("/etc/ceph/scripts/clear.sh")
    cmd_list.append("rm /var/lib/mysql/* -rf")
    for cmd in cmd_list:
        print "order >> %s"%cmd
        msg = os.popen(cmd)
        print "".join(msg.readlines())
        msg.close()
if __name__ == "__main__":
    main()
