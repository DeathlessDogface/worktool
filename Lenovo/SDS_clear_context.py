#!/usr/bin/python
import os


def run_cmd(cmd):
    print "order >>> %s" % cmd
    ret = os.popen(cmd)
    msg = ret.readlines()
    if msg:
        print msg
    ret.close()


def remove_package(name):
    with os.popen("rpm -qa|grep %s" % name) as p_name:
        while True:
            try:
                pkg = p_name.next()
                if pkg:
                    run_cmd("rpm -e --nodeps %s" % (pkg.strip("\n")))
            except StopIteration:
                break


def file_operation(*names, **kwargs):
    operation = kwargs.get("operation", "delete")
    path = kwargs.get("path", None)
    recursion = kwargs.get("recursion", True)
    if operation == "delete":
        if not path:
            path = os.path.curdir
        if os.path.isfile(path):
            os.remove(path)
            print "removed %s" % path
        elif os.path.isdir(path):
            if not names:
                os.rmdir(path)
                print "removed %s" % path
            elif names[0] == "*":
                os.rmdir(path)
                os.makedirs(path)
                print "removed %s/*" % path
            else:
                for root_dir, sub_dir, sub_names in os.walk(path):
                    for cur_name in sub_names:
                        for name in names:
                            if name in cur_name:
                                os.remove(os.path.join(root_dir, cur_name))
                                print "removed %s" % os.path.join(root_dir, cur_name)
                                continue
                    if not recursion:
                        break
    else:
        pass


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
        umount_disks = umount_disks.split(" ")
    else:
        umount_disks = ["/dev/sd%s" % i for i in list("abcdefghijkl")]
    for disk_path in umount_disks:
        run_cmd("umount %s" % disk_path)

    print "clean ceph..."
    run_cmd("/etc/ceph/scripts/clear.sh")
    run_cmd("/etc/ceph/scripts/disk_fs_mgmt.sh -O deletepartition")
    run_cmd("/etc/ceph/scripts/clear.sh")
    run_cmd("/etc/ceph/scripts/disk_fs_mgmt.sh -O deletepartition")

    print "remove config files..."
    file_operation("**", path="/var/lib/mysql/", operation='delete')
    file_operation("**", path="/Ceph/", operation='delete')
    file_operation("*", path="/etc/ceph/", operation='delete')
    file_operation("ceph.conf", ".keyring", ".cephdeploy.conf", path="/root/", operation='delete', recursion=False)
    file_operation("**", path="/usr/share/pyshared/ceph_deploy", operation='delete')
    file_operation("**", path="/usr/share/ceph-deploy", operation='delete')
    file_operation("**", path="/usr/lib/python2.6/site-packages/ceph_deploy", operation='delete')
    file_operation("**", path="/usr/share/pyshared/ceph-deploy", operation='delete')
    file_operation("ceph.conf", ".keyring", ".cephdeploy.conf", path="/root/", operation='delete', recursion=False)
    file_operation("ceph.conf", ".keyring", ".cephdeploy.conf", path="/root/", operation='delete', recursion=False)


if __name__ == "__main__":
    main()
