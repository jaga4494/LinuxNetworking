# -*- coding: utf-8 -*-
#!/usr/bin/python
from __future__ import print_function
import sys
import logging
import datetime
import libvirt
from xml.dom import minidom
import types
conn = libvirt.open('qemu:///system')
if conn == None:
    print('Failed to open connection to qemu:///system', file=sys.stderr)
    exit(1)

domains =  conn.listAllDomains(0)
if domains == None:
    print('Failed to find any domain ', file=sys.stderr)
    exit(1)

cpudict={}
for domain in domains:
    stats = domain.getCPUStats(True)
    cpudict[domain.name()]=stats[0]['cpu_time'] / 1000000000.


memdict={}
for domain in domains:
    stats  = domain.memoryStats()
    a=0
    b=0
    for name in stats:
        if name=='available':
            a=stats[name]
        elif name=='unused':
            b=stats[name]
    memdict[domain.name()]=a-b

def cpu():
    print('Sorted based on CPU Usage:')
    for key, value in sorted(cpudict.iteritems(), key=lambda (k,v): (v,k)):
        print("%s: %s" % (key, value))

def mem():
    print('Sorted based on MEM Usage:')
    for key, value in sorted(memdict.iteritems(), key=lambda (k,v): (v,k)):
        print("%s: %s" % (key, value))

options = {'CPU' : cpu,
           'MEM' : mem,
}

try:
    options[sys.argv[1]]()
except:
    print('Enter CPU or MEM as first argument!')

try:
    if int(sys.argv[2]):
        logger = logging.getLogger('cpulogs')
        hdlr = logging.FileHandler('./cpulogs.log')
        formatter = logging.Formatter('%(message)s')
        logger = logging.getLogger('cpulogs')
        logger.addHandler(hdlr)
        logger.setLevel(logging.WARNING)
        print('Logs generated:')
        for key, value in sorted(cpudict.iteritems(), key=lambda (k,v): (v,k)):
            if value > int(sys.argv[2]):
                logMessage=str(key) + '  ' + str(datetime.datetime.now()) + '  ' + str(value)
                print(logMessage)
                logger.error(logMessage)
except:
    print('Invalid Threshold Argument')
    exit(1)

conn.close()
exit(0)
