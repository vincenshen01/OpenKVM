import libvirt
import sys
from xml.dom import minidom


try:
    conn = libvirt.open('qemu+ssh://root@172.16.65.130/system?socket=/var/run/libvirt/libvirt-sock')
except libvirt.libvirtError:
    print('Failed to connect to the hypervisor')
    sys.exit(1)


storages = conn.listAllStoragePools()

for storage in storages:
    # print(storage.name())
    for volume in storage.listAllVolumes():
        # print(volume.name(), volume.path())
        print(volume.XMLDesc())
        caps = minidom.parseString(volume.XMLDesc())
        name = caps.getElementsByTagName('name')[0].firstChild.data
        capacity = caps.getElementsByTagName('capacity')[0].firstChild.data
        path = caps.getElementsByTagName('path')[0].firstChild.data
        format = caps.getElementsByTagName('format')[0].getAttribute('type')
        print(name, int(int(capacity)/1024/1024), path, format)
