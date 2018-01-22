import libvirt
import sys


if __name__ == '__main__':
    kvm_user = 'root'
    kvm_ip = '172.16.65.130'

    conn = libvirt.open('qemu+ssh://{user}@{ip}/system?socket=/var/run/libvirt/libvirt-sock'.format(
        user=kvm_user,
        ip=kvm_ip))

    # libvirt: QEMU Driver error : argument unsupported: QEMU guest agent is not configured
    dom = conn.lookupByName('vm001')
    if dom == None:
        print('Failed to get the domain object', file=sys.stderr)
    ifaces = dom.interfaceAddresses(libvirt.VIR_DOMAIN_INTERFACE_ADDRESSES_SRC_AGENT, 0)
    print("The interface IP addresses:")
    for (name, val) in ifaces.iteritems():
        if val['addrs']:
            for ipaddr in val['addrs']:
                if ipaddr['type'] == libvirt.VIR_IP_ADDR_TYPE_IPV4:
                    print(ipaddr['addr'] + " VIR_IP_ADDR_TYPE_IPV4")
                elif ipaddr['type'] == libvirt.VIR_IP_ADDR_TYPE_IPV6:
                    print(ipaddr['addr'] + " VIR_IP_ADDR_TYPE_IPV6")
    conn.close()