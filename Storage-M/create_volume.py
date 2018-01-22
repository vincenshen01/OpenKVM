import libvirt
import sys


def create_volume(conn, storage_pool_name, volume_name, format, capacity):
    storage_vol_xml = """
    <volume>
        <name>{name}.{format}</name>
        <allocation>0</allocation>
        <capacity unit="G">{capacity}</capacity>
        <target>
            <format type='{format}'/>
        </target>
    </volume>
    """.format(name=volume_name, format=format, capacity=capacity)

    storage_pool = conn.storagePoolLookupByName(storage_pool_name)
    if storage_pool is None:
        print('Failed to locate any StoragePool objects.', file=sys.stderr)
        exit(1)

    storage_vol = storage_pool.createXML(storage_vol_xml, 0)
    if storage_vol is not None:
        print('Create volume: {name}, capacity: {capacity} success!'.format(name=volume_name, capacity=capacity))
    else:
        print('Failed to create a StorageVol objects.', file=sys.stderr)
        exit(1)


if __name__ == '__main__':
    kvm_user = 'root'
    kvm_ip = '172.16.65.130'
    storage_pool_name = 'nfsFile'
    volume_name = 'vm010'
    volume_format = 'qcow2'
    volume_capacity = 10

    conn = libvirt.open('qemu+ssh://{user}@{ip}/system?socket=/var/run/libvirt/libvirt-sock'.format(
        user=kvm_user,
        ip=kvm_ip
    ))
    create_volume(conn, storage_pool_name, volume_name, volume_format, volume_capacity)
    conn.close()