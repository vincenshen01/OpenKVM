import libvirt
import lxml


conn = libvirt.open('qemu+ssh://root@172.16.65.130/system?socket=/var/run/libvirt/libvirt-sock')
# pools = conn.listAllStoragePools(0)
#
# for pool in pools:
#
#     #check if pool is active
#     if pool.isActive() == 0:
#         #activate pool
#         pool.create()
#
#     stgvols = pool.listVolumes()
#     print('Storage pool: '+pool.name())
#     for stgvol in stgvols :
#         print('  Storage vol: '+stgvol)


print(conn.getHostname())
print(conn.getCPUMap())
print(conn.getVersion())
print(conn.getFreeMemory())
print(conn.getMemoryStats(0))
print(conn.getCPUStats(0))
print(conn.listNetworks())

print(conn.getInfo())
print(conn.listDomainsID())

print(dir(conn.lookupByID(4)))
domain = conn.lookupByID(4)
print(domain.memoryStats())
print(domain.info())
print(domain.name())