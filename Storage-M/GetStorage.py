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
    print(storage.name())
    print(dir(storage))
    # print(storage.XMLDesc())
    # print(storage.name())
    # print(storage.info())
    # print(storage.UUIDString())

# storage_pool = conn.storagePoolLookupByName('nfsFile')
