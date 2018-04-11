#!/usr/bin/python
import os
def run_cmd(cmd):
    print "order >>> %s"%cmd
    ret = os.popen(cmd)
    msg = ret.readlines()
    if msg:
        print msg
    ret.close
def remove_package(name):
    pkg_list=[]
    with os.popen("rpm -qa|grep %s"%name) as p_name:
        while True:
            try:
                pkg = p_name.next()
                if pkg:
                    run_cmd("rpm -e --nodeps %s"%(pkg.strip("\n")))
            except StopIteration:
                break

def main():
    print "stop ceph..."
    run_cmd('/etc/init.d/ceph -a -c /etc/ceph/ceph.conf stop')
    print "remove packages..."
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
        "mariadb",
        "ntp",
        "ceph",
    ]:
        remove_package(pkg)
    print "umount disk..."    
    umount_disks = raw_input("write the name of path need to umount,default is a~l:")
    if umount_disks:
        umount_disks=umount_disks.split(" ")
    else:
        umount_disks=["/dev/sd%s"% i for i in list("abcdefghijkl")]
    for disk_path in umount_disks:
        run_cmd("umount %s"%disk_path)
    print "clean ceph..."
    run_cmd("/etc/ceph/scripts/clear.sh")
    run_cmd("/etc/ceph/scripts/disk_fs_mgmt.sh -O deletepartition")
    run_cmd("/etc/ceph/scripts/clear.sh")
    run_cmd("/etc/ceph/scripts/disk_fs_mgmt.sh -O deletepartition")
    print "remove config files..."
    for f_path in [
        "/var/lib/mysql/*",
        "/Ceph/*",
        "/root/ceph.*",
        "/etc/ceph/",
        "$(ls /root/ | grep *.keyring)",
    ]:
        run_cmd("rm %s -rf"%f_path)
if __name__ == "__main__":
    main()
