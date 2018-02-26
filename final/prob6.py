#!/usr/bin/python
from __future__ import print_function
import sys
import libvirt
from xml.dom import minidom
conn = libvirt.open('qemu:///system')
if conn == None:
    print('Failed to open connection to qemu:///system', file=sys.stderr)
    exit(1)
print("----------------")
print("Host Information")
print("----------------")
host = conn.getHostname()
print('Hostname:'+host)
nodeinfo = conn.getInfo()
print('Memory size: '+str(nodeinfo[1])+'MB')
print('Number of CPUs: '+str(nodeinfo[2]))
print('MHz of CPUs: '+str(nodeinfo[3]))
print('Number of NUMA nodes: '+str(nodeinfo[4]))
print('Number of CPU sockets: '+str(nodeinfo[5]))
print('Number of CPU cores per socket: '+str(nodeinfo[6]))
print('Number of CPU threads per core: '+str(nodeinfo[7]))
print('Virtualization type: '+conn.getType())
vcpus = conn.getMaxVcpus(None)
print('Maximum support virtual CPUs: '+str(vcpus))
vcpus = conn.getMaxVcpus(None)
print('Maximum support virtual CPUs: '+str(vcpus))
dom=0
try:
    domName = sys.argv[1]

except:
    print('Invalid Argument')
    exit(1)
try:
    dom = conn.lookupByName(domName)
except:
    sys.exit(1)

id = dom.ID()
print("------------------------")
print("Guest Domain Information")
print("------------------------")
print('Domain Name ' + domName)

if id == -1:
    print('The domain is not running so has no ID.')
else:
    print('The ID of the domain is ' + str(id))
uuid = dom.UUIDString()
print('The UUID of the domain is ' + uuid)
cpus = dom.maxVcpus()
if cpus != -1:
    print('The max Vcpus for domain is ' + str(cpus))
else:
    print('There was an error.')
state, reason = dom.state()

if state == libvirt.VIR_DOMAIN_NOSTATE:
    print('The state is VIR_DOMAIN_NOSTATE')
elif state == libvirt.VIR_DOMAIN_RUNNING:
    print('The state is VIR_DOMAIN_RUNNING')
elif state == libvirt.VIR_DOMAIN_BLOCKED:
    print('The state is VIR_DOMAIN_BLOCKED')
elif state == libvirt.VIR_DOMAIN_PAUSED:
    print('The state is VIR_DOMAIN_PAUSED')
elif state == libvirt.VIR_DOMAIN_SHUTDOWN:
    print('The state is VIR_DOMAIN_SHUTDOWN')
elif state == libvirt.VIR_DOMAIN_SHUTOFF:
    print('The state is VIR_DOMAIN_SHUTOFF')
elif state == libvirt.VIR_DOMAIN_CRASHED:
    print('The state is VIR_DOMAIN_CRASHED')
elif state == libvirt.VIR_DOMAIN_PMSUSPENDED:
    print('The state is VIR_DOMAIN_PMSUSPENDED')
else:
    print(' The state is unknown.')

state, maxmem, mem, cpus, cput = dom.info()
print('The max memory is ' + str(maxmem))
print('The number of cpus is ' + str(cpus))
print('The cpu time is ' + str(cput))
type = dom.OSType()
print('The OS type of the domain is "' + type + '"')
conn.close()
exit(0)
