import libvirt
import sys
from xml.dom import minidom

try:
    conn = conn = libvirt.open('qemu+ssh://root@172.16.65.130/system?socket=/var/run/libvirt/libvirt-sock')
except libvirt.libvirtError:
    print('Failed to connect to the hypervisor')
    sys.exit(1)

try:
    capsXML = conn.getCapabilities()
    print(capsXML)
except libvirt.libvirtError:
    print('Failed to request capabilities')
    sys.exit(1)

caps = minidom.parseString(capsXML)

topology = caps.getElementsByTagName('topology')[0]
cpu_sockets = topology.getAttribute("sockets")
cpu_cores = topology.getAttribute("cores")
print(cpu_sockets, cpu_cores)

memory_ele = caps.getElementsByTagName("memory")[0]
print(memory_ele.firstChild.data)






host = caps.getElementsByTagName('host')[0]
cells = host.getElementsByTagName('cells')[0]
total_cpus = cells.getElementsByTagName('cpu').length

socketIds = []
siblingsIds = []

socketIds = [proc.getAttribute('socket_id')
             for proc in cells.getElementsByTagName('cpu')
             if proc.getAttribute('socket_id') not in socketIds ]

siblingsIds = [ proc.getAttribute('siblings')
                for proc in cells.getElementsByTagName('cpu')
                if proc.getAttribute('siblings') not in siblingsIds ]

# print("Host topology")
# print("NUMA nodes:", cells.getAttribute('num'))
# print("   Sockets:", len(set(socketIds)))
# print("     Cores:", len(set(siblingsIds)))
# print("   Threads:", total_cpus)