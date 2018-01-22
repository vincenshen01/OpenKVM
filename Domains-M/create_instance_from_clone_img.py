import libvirt
import sys

volume_xml = '''
<volume>
    <name>{name}.img</name>
    <allocation>0</allocation>
    <capacity unit="G">{capacity}</capacity>
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

instance_xml = """
<domain type='kvm'>
    <name>{name}</name>               
    <memory unit='GiB'>{memory}</memory>
    <currentMemory unit='GiB'>{memory}</currentMemory>
    <vcpu>{cpu}</vcpu>
    <os>
        <type arch='x86_64' machine='pc'>hvm</type>
        <boot dev='hd'/>
    </os>
    <clock offset='localtime'/>
    <on_poweroff>destroy</on_poweroff>
    <on_reboot>restart</on_reboot>
    <on_crash>destroy</on_crash>
    <devices>
        <emulator>/usr/bin/kvm-spice</emulator>
        <disk type='file' device='disk'>
            <driver name='qemu' type='qcow2'/>
            <source file='{path}'/>
            <target dev='hda' bus='scsi'/>
        </disk>
        <interface type='bridge'>
            <source bridge='{network}'/>
        </interface>
        <input type='mouse' bus='ps2'/>
        <input type='keyboard' bus='ps2'/>
        <graphics type='vnc' port='-1' autoport='yes' listen = '0.0.0.0' keymap='en-us'/>
    </devices>
</domain>
"""

"""虚拟机配置文件路径：/etc/libvirt/qemu/**.xml"""


def clone_volume_from_img(conn, img, xml, storage_name):
    storage_pool = conn.storagePoolLookupByName(storage_name)
    for volume in storage_pool.listAllVolumes():
        if volume.name() == img:
            # Clone the existing storage volume
            new_volume = storage_pool.createXMLFrom(xml, volume, 0)
            if new_volume is not None:
                print('Clone IMG Success!')
                return new_volume.path()
            else:
                print('Clone Error!')
                sys.exit(1)


def create_instance(conn, instance_xml):
    dom = conn.defineXML(instance_xml)
    instance_res = dom.create()
    if instance_res is not None:
        print('Create Instance Success!')
    else:
        print('Create Instance Error!')
        sys.exit(1)


if __name__ == '__main__':
    kvm_ip = '172.16.65.130'
    kvm_user = 'root'
    kvm_storage_pool = 'nfsFile'
    # 使用libvirt.open的前提条件是需要实现Root无密码访问"""
    conn = libvirt.open('qemu+ssh://{user}@{ip}/system?socket=/var/run/libvirt/libvirt-sock'.format(
        user=kvm_user,
        ip=kvm_user
    ))
    if conn is None:
        print('Failed to connect to {}'.format(kvm_ip), file=sys.stderr)

    # Instance Params
    instance_img = 'cirros-0.4.0-x86_64-disk.img'
    instance_img_space = 10  # GB
    instance_path = '/nfsFile/images'
    instance_name = 'vm006'
    instance_network = 'brvlan100'
    instance_cpu = 1
    instance_memory = 1
    instance_volume_capacity = 10  # GB

    # Clone img
    volume_xml = volume_xml.format(name=instance_name,
                                   capacity=instance_volume_capacity,
                                   path=instance_path)
    volume_path = clone_volume_from_img(conn, instance_img, volume_xml, kvm_storage_pool)

    # Create Instance
    instance_xml = instance_xml.format(name=instance_name,
                                       cpu=instance_cpu,
                                       memory=instance_memory,
                                       path=volume_path,
                                       network=instance_network)
    create_instance(conn, instance_xml)

    # libvirt disconnect
    conn.close()