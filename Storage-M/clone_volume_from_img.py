import libvirt
import sys


new_volume_xml = '''
<volume>
    <name>{name}.img</name>
    <allocation>0</allocation>
    <capacity unit="G">{capacity</capacity>
    <target>
        <format type='qcow2'/>
        <path>{path}/{name}.img</path>
        <permission>
            <owner>107</owner>
            <group>107</group>
            <mode>0744</mode>
            <label>virt_image_t</label>
        </permission>
    </target>
</volume>
'''


def clone_volume(conn, storage_pool_name, volume_xml, img_name):
    storage_pool = conn.storagePoolLookupByName(storage_pool_name)
    for volume in storage_pool.listAllVolumes():
        if volume.name() == img_name:
            # Clone the existing storage volume
            new_volume = storage_pool.createXMLFrom(volume_xml, volume)
            if new_volume is not None:
                print('Clone Success!')
                break

if __name__ == '__main__':
    kvm_user = 'root'
    kvm_ip = '172.16.65.130'
    storage_pool_name = 'nsfFile'
    img_name = 'cirros-0.4.0-x86_64-disk.img'
    volume_name = 'vm001'
    volume_capacity = 10
    volume_path = '/nfsFile/images'

    conn = libvirt.open('qemu+ssh://{user}@{ip}/system?socket=/var/run/libvirt/libvirt-sock'.format(
        user=kvm_user,
        ip=kvm_ip
    ))
    new_volume_xml = new_volume_xml.format(name=volume_name,
                                           capacity=volume_capacity,
                                           path=volume_path)
    clone_volume(conn, storage_pool_name, new_volume_xml, img_name)

    conn.close()