import libvirt
import sys


if __name__ == '__main__':
    kvm_user = 'root'
    kvm_ip = '172.16.65.130'

    conn = libvirt.open('qemu+ssh://{user}@{ip}/system?socket=/var/run/libvirt/libvirt-sock'.format(
        user=kvm_user,
        ip=kvm_ip
    ))

    interfaces = conn.listInterfaces()
    for interface in interfaces:
        print(dir(interface))
        print(interface)

    interfaces_2 = conn.listDefinedInterfaces()
    for interface in interfaces_2:
        print(interfaces)

    interface_obj = conn.interfaceLookupByName('ens33.100')
    print(interface_obj.name())
    conn.close()