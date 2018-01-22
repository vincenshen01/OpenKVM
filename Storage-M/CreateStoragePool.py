def createStoragePool(conn):
    xmlDesc = """
    <pool type='dir'>
      <name>guest_images_storage_pool</name>
      <uuid>8c79f996-cb2a-d24d-9822-ac7547ab2d01</uuid>
      <capacity unit='bytes'>4306780815</capacity>
      <allocation unit='bytes'>237457858</allocation>
      <available unit='bytes'>4069322956</available>
      <source>
      </source>
      <target>
        <path>/path/to/guest_images</path>
        <permissions>
          <mode>0755</mode>
          <owner>-1</owner>
          <group>-1</group>
        </permissions>
      </target>
    </pool>"""

    pool = conn.storagePoolDefineXML(xmlDesc, 0)

    # set storage pool autostart
    pool.setAutostart(1)
    return pool