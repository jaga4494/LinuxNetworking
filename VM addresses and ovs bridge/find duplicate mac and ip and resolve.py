# -*- coding: utf-8 -*-
#!/usr/bin/python

from __future__ import print_function
import sys
from xml.dom import minidom
from subprocess import call
import os
import base64
import collections
import random
import xml.etree.ElementTree as ET
import libvirt
import operator
import re
import subprocess
import paramiko

conn = libvirt.open('qemu:///system')
if conn == None:
    print('Failed to open connection to qemu:///system', file=sys.error)
    exit(1)

domainIDs = conn.listDomainsID()
print("Available Domains: ", domainIDs)

mac_dup_list =[]
ip_dup_list = []
iplistofmac = []
ip_addr_list = []
mac_addr_list=[]
mac_ip_dict={}

for dom in domainIDs:
        xml1 = conn.lookupByID(dom).XMLDesc(0)
        xml = minidom.parseString(xml1)
        ifctypes = xml.getElementsByTagName('interface')
        for ifctype in ifctypes:
                #print('interface: type='+ifctype.getAttribute('type'))
                ifcnodes = ifctype.childNodes
                #print(type(ifcnodes))
        mac_addr = ''
        for ifcnode in ifcnodes:
                if ifcnode.nodeName[0:1] != '#':
                #print('  '+ifcnode.nodeName)
                        for field in ifcnode.attributes.keys():
                        #print("field:"+field)
                                if field == "address":
                                        print('    '+ifcnode.attributes[field].name+' = '+ ifcnode.attributes[field].value)
                                        mac_addr = ifcnode.attributes[field].value
                                        if mac_addr in mac_addr_list:
                                                mac_dup_list.append(mac_addr)
                                        else:
                                                mac_addr_list.append(mac_addr)

                                        print("Mac address: ", mac_addr)
                                        #ip_addr_list.append(os.system('/usr/sbin/arp -n | grep ' + mac_addr + ' | awk \'{print $1}\''))
                                        #print("Output of proc:", proc)
                                        #print("IP list:", ip_addr_list)
                                        output = (subprocess.Popen("/usr/sbin/arp -n | grep %s | awk \'{print $1}\'" % mac_addr, shell=True, out=subprocess.PIPE).out.read())
                                        output = output.split('\n')[:-1]
                                        if output in ip_addr_list:
                                                ip_dup_list.append(output)
                                        else:
                                                ip_addr_list.append(output)
                                        mac_ip_dict[str(mac_addr)] = output
                                        print("IP list: ",output)
                                        print("IP addresses: ",ip_addr_list)
                                        print("MAC and IP list: ",mac_ip_dict)

for dupmac in mac_dup_list:
        iplistofmac=mac_ip_dict[dupmac]
        for single_ip in iplistofmac:
                    ipforssh=single_ip

                    try:
                            pri_file = os.path.expanduser('~/.ssh/id_rsa')
                            pri_key = paramiko.RSAKey.from_private_key_file(pri_file)
                            #client.connect("192.168.130.115", username = 'root', pkey = pri_key)
                            ssh = paramiko.SSHClient()
                            ssh.load_system_host_keys()
                            ssh.set_missing_host_key_policy(paramiko.WarningPolicy())
                            print('Connection Started !!!')
                            ssh.connect(ipforssh, username = 'root', pkey = pri_key, look_for_keys = True)
                            #client.connect(blade, 22, username, password)
                            in, out, error  = ssh.exec_command("ip -o addr show scope global | awk \'{split($4, a, \"/\"); print $2\" : \"a[1]}\' | grep %s | awk \'{print $1}\'" %ipforssh )
                            #in, out, error = ssh.exec_command("ip address show")
                            ifcname = str(out.readlines()[0]).replace('\n','')
                            print('Interface Name is: ', ifcname)
                            mac_new =( "73:14:33:51:%02x:%02x" % (
                                    random.randint(0, 255),
                                    random.randint(0, 255),
                                    ))
                            print("Randomly generated MAC: ", mac_new)
                            #in, out, error = ssh.exec_command("ip link set dev %s down" % ifcname)
                            in, out, error = ssh.exec_command("ip link set dev %s address %s" % (ifcname,mac_new))
                            #in, out, error = ssh.exec_command("ip link set dev %s up" % ifcname)
                            in, out, error = ssh.exec_command("ip address show %s" % ifcname)
                            print("Output:", out.readlines())
                    except Exception, e:
                            print('Exception!!')
                            traceback.print_exc()

ssh.close()
conn.close()
exit(0)
