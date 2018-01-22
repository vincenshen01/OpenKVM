import libvirt
import sys


def create_network(conn, name, forward_dev, forward_mode, gateway_ip, net_mask, start_ip, end_ip):
    network_xml = '''
    <network>
      <name>{name}</name>
      <forward dev='{forward_dev}' mode='{forward_mode}'>
        <interface dev='{forward_dev}'/>
      </forward>
      <bridge name='{name}' stp='off' delay='0'/>
      <domain name='{name}'/>
      <ip address='{gateway_ip}' netmask='{net_mask}'>
        <dhcp>
          <range start='{dhcp_start_ip}' end='{dhcp_end_ip}'/>
        </dhcp>
      </ip>
    </network>'''.format(name=name,
                         forward_dev=forward_dev,
                         forward_mode=forward_mode,
                         gateway_ip=gateway_ip,
                         net_mask=net_mask,
                         dhcp_start_ip=start_ip,
                         dhcp_end_ip=end_ip,
                         )
    network_obj = conn.networkDefineXML(network_xml)    # Define an inactive persistent virtual network
    network_obj.setAutostart(1)
    network_obj.create()


if __name__ == '__main__':
    kvm_user = 'root'
    kvm_ip = '172.16.65.130'

    conn = libvirt.open('qemu+ssh://{user}@{ip}/system?socket=/var/run/libvirt/libvirt-sock'.format(
        user=kvm_user,
        ip=kvm_ip))

    name = "VLAN100"
    forward_dev = 'brvlan100'
    forward_mode = 'route'  # route or nat
    gateway_ip = '192.168.100.1'
    net_mask = '255.255.255.0'
    dhcp_start_ip = '192.168.100.128'
    dhcp_end_ip = '192.168.100.254'
    create_network(conn, name, forward_dev, forward_mode, gateway_ip, net_mask, dhcp_start_ip, dhcp_end_ip)

