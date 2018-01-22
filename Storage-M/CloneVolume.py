import libvirt
import sys

conn = libvirt.open('qemu+ssh://root@172.16.65.130/system?socket=/var/run/libvirt/libvirt-sock')


new_volume_xml = '''
<volume>
    <name>cirros-test-02-disk.img</name>
    <allocation>0</allocation>
    <capacity unit="G">10</capacity>
    <target>
        <format type='qcow2'/>
        <path>/nfsFile/images/cirros-test-02-disk.img</path>
        <permission>
            <owner>107</owner>
            <group>107</group>
            <mode>0744</mode>
            <label>virt_image_t</label>
        </permission>
    </target>
</volume>
'''

storages = conn.listAllStoragePools()

for storage in storages:
    for volume in storage.listAllVolumes():
        if volume.name() == 'cirros-0.4.0-x86_64-disk.img':
            # Clone the existing storage volume
            new_volume = storage.createXMLFrom(new_volume_xml, volume, 0)
            if new_volume is not None:
                print('Clone Success!')
                break

