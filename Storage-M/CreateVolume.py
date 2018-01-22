import libvirt
import sys

conn = libvirt.open('qemu+ssh://root@172.16.65.130/system?socket=/var/run/libvirt/libvirt-sock')

storage_vol_xml = """
<volume>
    <name>vm006.qcow2</name>
    <allocation>0</allocation>
    <capacity unit="G">10</capacity>
    <target>
        <format type='qcow2'/>
    </target>

</volume>
"""

pool = 'nfsFile'

pool = conn.storagePoolLookupByName(pool)
if pool == None:
    print('Failed to locate any StoragePool objects.', file=sys.stderr)
    exit(1)
storage_vol = pool.createXML(storage_vol_xml, 0)
storage_vol.path()
if storage_vol == None:
    print('Failed to create a StorageVol objects.', file=sys.stderr)
    exit(1)

conn.close()