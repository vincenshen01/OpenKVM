import libvirt


def create_storage_pool(conn, name, path):
    xmlDesc = """
    <pool type='dir'>
      <name>{name}</name>
      <target>
        <path>{path}</path>
        <permissions>
          <mode>0755</mode>
          <owner>-1</owner>
          <group>-1</group>
        </permissions>
      </target>
    </pool>""".format(name=name, path=path)

    # create a new persistent storage pool
    pool = conn.storagePoolCreateXML(xmlDesc)

    # set storage pool autostart
    pool.setAutostart(1)
    pool.isActive()
    return pool


if __name__ == '__main__':
    kvm_user = 'root'
    kvm_ip = '172.16.65.130'
    storage_pool_name = 'NewStorage'
    storage_path = '/nfsFile'

    conn = libvirt.open('qemu+ssh://{user}@{ip}/system?socket=/var/run/libvirt/libvirt-sock'.format(
        user=kvm_user,
        ip=kvm_ip))

    pool = create_storage_pool(conn, storage_pool_name, storage_path)
    if pool is not None:
        print('Create Storage Pool: {name} Success!'.format(name=storage_pool_name))
    conn.close()