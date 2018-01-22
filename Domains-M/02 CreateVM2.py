import libvirt
import sys


xml_config = """
<domain type='kvm'>
    <name>vm003</name>               
    <memory unit='GiB'>1</memory>
    <currentMemory unit='GiB'>1</currentMemory>
    <vcpu>1</vcpu>
    <os>
        <type arch='x86_64' machine='pc'>hvm</type>
        <boot dev='hd'/>
        <boot dev='cdrom'/>
    </os>
    <clock offset='localtime'/>
    <on_poweroff>destroy</on_poweroff>
    <on_reboot>restart</on_reboot>
    <on_crash>destroy</on_crash>
    <devices>
        <emulator>/usr/bin/kvm-spice</emulator>
        <disk type='file' device='disk'>
            <driver name='qemu' type='qcow2'/>
            <source file='/nfsFile/images/cirros-test-02-disk.img'/>
            <target dev='hda' bus='scsi'/>
        </disk>
        <interface type='network'>
            <source network='default'/>
        </interface>
        <input type='mouse' bus='ps2'/>
        <input type='keyboard' bus='ps2'/>
        <graphics type='vnc' port='-1' autoport='yes' listen = '0.0.0.0' keymap='en-us'/>
    </devices>
</domain>
"""

"""虚拟机配置文件路径：/etc/libvirt/qemu/**.xml"""

conn = libvirt.open('qemu+ssh://root@172.16.65.130/system?socket=/var/run/libvirt/libvirt-sock')
dom = conn.defineXML(xml_config)
dom.create()

print(dom.name())

conn.close()