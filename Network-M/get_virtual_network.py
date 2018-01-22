import libvirt
import sys


if __name__ == '__main__':
    kvm_user = 'root'
    kvm_ip = '172.16.65.130'

    conn = libvirt.open('qemu+ssh://{user}@{ip}/system?socket=/var/run/libvirt/libvirt-sock'.format(
        user=kvm_user,
        ip=kvm_ip
    ))

    # network_list = conn.listAllNetworks()
    #
    # for network in network_list:
    #     print(network.name())

    network_obj = conn.networkLookupByName('VLAN100')
    # print(dir(network_obj))
    # print(network_obj.name())
    # print(network_obj.bridgeName())
    print(network_obj.DHCPLeases())
    print(network_obj.XMLDesc())
    conn.close()