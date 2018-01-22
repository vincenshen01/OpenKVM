import libvirt
import sys
import os
import pdb

def usage():
   print('Usage: %s DOMAIN' % sys.argv[0])
   print('       Print information about the domain DOMAIN')

def print_section(title):
    print("\n%s" % title)
    print("=" * 60)

def print_entry(key, value):
    print("%-10s %-10s" % (key, value))

def print_xml(key, ctx, path):
    res = ctx.xpathEval(path)
    if res is None or len(res) == 0:
        value="Unknown"
    else:
        value = res[0].content
    print_entry(key, value)
    return value


name = "vm002"

# Connect to libvirt
conn = libvirt.open('qemu+ssh://root@172.16.65.130/system?socket=/var/run/libvirt/libvirt-sock')

if conn is None:
    print('Failed to open connection to the hypervisor')
    sys.exit(1)

try:
    dom = conn.lookupByName(name)
    # Annoyiingly, libvirt prints its own error message here
except libvirt.libvirtError:
    print("Domain %s is not running" % name)
    sys.exit(0)

info = dom.info()
print_section("Domain info")
print_entry("State:", info[0])
print_entry("MaxMem:", info[1])
print_entry("UsedMem:", info[2])
print_entry("VCPUs:", info[3])

# Read some info from the XML desc
xmldesc = dom.XMLDesc(0)


print_section("Devices")

print(xmldesc)
