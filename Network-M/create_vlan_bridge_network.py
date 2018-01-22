import libvirt
import sys


def create_vlan_interface(conn, interface, vlan_id):
    vlan_xml ='''
    <interface type="vlan" name="{interface}.{vlan_id}">
        <start mode="onboot"/>
        <vlan tag="{vlan_id}">
            <interface name="{interface}"/>
        </vlan>
    </interface>'''.format(interface=interface, vlan_id=vlan_id)
    vlan_obj = conn.interfaceDefineXML(vlan_xml)
    if vlan_obj:
        vlan_obj.create()   # set the network active
        print('create vlan interface success!')


def create_bridge_interface(conn, bridge_name, bridge_interface ):
    bridge_xml = '''
    <interface type="bridge" name="{bridge_name}">
    <start mode="onboot"/>
    <mtu size="1500"/>
    <bridge stp="off" delay="0.01">
        <interface type="ethernet" name="{bridge_interface}"/>
    </bridge>
    </interface>'''.format(bridge_name=bridge_name, bridge_interface=bridge_interface)
    bridge_obj = conn.interfaceDefineXML(bridge_xml)
    if bridge_obj:
        bridge_obj.create()
        print('create bridge success!')


if __name__ == '__main__':
    kvm_user = 'root'
    kvm_ip = '172.16.65.130'

    conn = libvirt.open('qemu+ssh://{user}@{ip}/system?socket=/var/run/libvirt/libvirt-sock'.format(
        user=kvm_user,
        ip=kvm_ip
    ))

    interface = 'ens33'
    vlan_id = '104'
    create_vlan_interface(conn, interface, vlan_id)

    bridge_name = 'brvlan104'
    bridge_interface = interface + '.' + vlan_id
    create_bridge_interface(conn, bridge_name, bridge_interface)
    conn.close()