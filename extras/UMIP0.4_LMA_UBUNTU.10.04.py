#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import os
import subprocess
import getopt

from subprocess  import *
from netaddr import *

g_path = os.getcwd()
g_path = os.path.dirname(sys.argv[0]) + "/.."
g_path = os.path.abspath(g_path)

try:
    opts, args = getopt.getopt(sys.argv[1:], "prd", ["pcap=", "runversion=", "pmipdir="])
except getopt.GetoptError, err:
    # print help information and exit:
    print str(err) # will print something like "option -a not recognized"
    sys.exit(2)

g_pcap = "no"
g_run_version = "1"

for o,p in opts:
  if o in ('-p','--pcap'):
     g_pcap = p
  elif o in ['-r','--runversion']:
     g_run_version = str(p)
  elif o in ['-d','--pmipdir']:
     g_path = p

############################################################################################
g_file_config=g_path+"/extras/example-lma.conf"
############################################################################################


g_RFC5213FixedMAGLinkLocalAddressOnAllAccessLinks = IPAddress('0::0')
g_RFC5213FixedMAGLinkLayerAddressOnAllAccessLinks = " "
g_LmaAddress                                      = IPAddress('0::0')
g_LmaPmipNetworkDevice                            = ""
g_LmaCoreNetworkAddress                           = IPAddress('0::0')
g_LmaCoreNetworkDevice                            = ""
g_Mag1AddressIngress                              = IPAddress('0::0')
g_Mag1AddressEgress                               = IPAddress('0::0')
g_Mag2AddressIngress                              = IPAddress('0::0')
g_Mag2AddressEgress                               = IPAddress('0::0')
g_Mag3AddressIngress                              = IPAddress('0::0')
g_Mag3AddressEgress                               = IPAddress('0::0')



g_fhandle = open(g_file_config, 'r')
g_fcontent = g_fhandle.read()
g_fhandle.close()

lines = g_fcontent.splitlines()
for line in lines:
    line = line.rstrip().lstrip()
    line = line.rstrip(';')
    split = line.split(' ')
    element = split[-1]
    element = element.strip('"')
    if 'RFC5213FixedMAGLinkLocalAddressOnAllAccessLinks' in line:
        print line
        g_RFC5213FixedMAGLinkLocalAddressOnAllAccessLinks = IPAddress(element)

    elif 'RFC5213FixedMAGLinkLayerAddressOnAllAccessLinks' in line:
        print line
        g_RFC5213FixedMAGLinkLayerAddressOnAllAccessLinks = element
    elif 'LmaAddress' in line:
        print line
        g_LmaAddress = IPAddress(element)
    elif 'LmaPmipNetworkDevice' in line:
        print line
        g_LmaPmipNetworkDevice = element
    elif 'LmaCoreNetworkAddress' in line:
        print line
        g_LmaCoreNetworkAddress = IPAddress(element)
    elif 'LmaCoreNetworkDevice' in line:
        print line
        g_LmaCoreNetworkDevice = element
    elif 'Mag1AddressIngress' in line:
        print line
        g_Mag1AddressEgress = IPAddress(element)
    elif 'Mag1AddressEgress' in line:
        print line
        g_Mag1AddressEgress = IPAddress(element)
    elif 'Mag2AddressIngress' in line:
        print line
        g_Mag2AddressEgress = IPAddress(element)
    elif 'Mag2AddressEgress' in line:
        print line
        g_Mag2AddressEgress = IPAddress(element)
    elif 'Mag3AddressIngress' in line:
        print line
        g_Mag3AddressEgress = IPAddress(element)
    elif 'Mag3AddressEgress' in line:
        print line
        g_Mag3AddressEgress = IPAddress(element)

if g_Mag1AddressIngress.format() != IPAddress('::').format():
    command = "ip -6 route del " + g_Mag1AddressIngress.format() + "/64"
    print command
    os.system(command)
if g_Mag2AddressIngress.format() != IPAddress('::').format():
    command = "ip -6 route del " + g_Mag2AddressIngress.format() + "/64"
    print command
    os.system(command)
if g_Mag3AddressIngress.format() != IPAddress('::').format():
    command = "ip -6 route del " + g_Mag3AddressIngress.format() + "/64"
    print command
    os.system(command)

for i in range (1 , 255):
    command = "ip -6 tunnel del ip6tnl" + str(i) + " >/dev/null 2>&1"
    os.system(command)

command = "ip -6 addr del " + g_LmaAddress.format() + "/64 dev " + g_LmaPmipNetworkDevice
print command
os.system(command)

command = "rmmod ip6_tunnel"
print command
os.system(command)
command = "rmmod tunnel6"
print command
os.system(command)



command = "echo \"0\" > /proc/sys/net/ipv6/conf/all/accept_ra"
print command
os.system(command)
command = "echo \"0\" > /proc/sys/net/ipv6/conf/" + g_LmaPmipNetworkDevice + "/accept_ra"
print command
os.system(command)
command = "echo \"0\" > /proc/sys/net/ipv6/conf/" + g_LmaCoreNetworkDevice + "/accept_ra"
print command
os.system(command)
command = "echo \"1\" > /proc/sys/net/ipv6/conf/all/forwarding"
print command
os.system(command)



command = "ip -6 addr add " + g_LmaAddress.format() + "/64 dev " + g_LmaPmipNetworkDevice
print command
os.system(command)
command = "ip -6 addr add " + g_LmaCoreNetworkAddress.format()+"/64 dev "+ g_LmaCoreNetworkDevice
print command
os.system(command)

if g_Mag1AddressIngress != IPAddress('::'):
    command = "ip -6 route add " + Mag1AddressIngress.format() + "/64 via " + Mag1AddressEgress.format() + " dev " + g_LmaPmipNetworkDevice
    print command
    os.system(command)
    # just to resolve, avoid ping6 since it is used for sync
    command = "ssh -6 root@[" + Mag1AddressIngress.format() + "] \"ls /root\""
    print command
    os.system(command)


if g_Mag2AddressIngress != IPAddress('::'):
    command = "ip -6 route add " + Mag2AddressIngress.format() + "/64 via " + Mag2AddressEgress.format() + " dev " + g_LmaPmipNetworkDevice
    print command
    os.system(command)
    # just to resolve, avoid ping6 since it is used for sync
    command = "ssh -6 root@[" + Mag2AddressIngress.format() + "] \"ls /root\""
    print command
    os.system(command)

if g_Mag3AddressIngress != IPAddress('::'):
    command = "ip -6 route add " + Mag3AddressIngress.format() + "/64 via " + Mag3AddressEgress.format() + " dev " + g_LmaPmipNetworkDevice
    print command
    os.system(command)
    # just to resolve, avoid ping6 since it is used for sync
    command = "ssh -6 root@[" + Mag3AddressIngress.format() + "] \"ls /root\""
    print command
    os.system(command)

command = "modprobe ip6_tunnel"
print command
os.system(command)
command = "modprobe tunnel6"
print command
os.system(command)

command = "pkill -9 pmip6d"
print command
os.system(command)

if g_pcap == "yes":
	command = "xhost + ; export DISPLAY=:0.0 ; sync; wireshark -i eth0 -k -n -w  "+ g_path + "/logs/lma2mags."+g_run_version+".pcap &"
	value = os.system(command)
	print value

	command = "xhost + ; export DISPLAY=:0.0 ; sync; wireshark -i eth1 -k -n -w  "+ g_path + "/logs/lma2cn."+g_run_version+".pcap  &"
	value = os.system(command)
	print value


command = '/usr/local/sbin/pmip6d -c ' + g_file_config
print command
subprocess.call(command, shell=True)

