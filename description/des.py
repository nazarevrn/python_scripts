#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-
import telnetlib
import time
import getpass
import sys
from collections import OrderedDict

USER_TELESIS = 'manager'
PASSWORD_TELESIS = 'friend'
USER_CORE = 'nazarev'
print('\n')
IP = raw_input("Enter target switch's IP: ")
IP_CORE = raw_input("Enter core switch's IP: ")

PASSWORD_CORE = getpass.getpass("Enter core password: ")

telesis = telnetlib.Telnet(IP)
telesis.read_until("User Name:") #for cisco it will be 'Username'
telesis.write(USER_TELESIS + '\n')
telesis.read_until("Password:")
telesis.write(PASSWORD_TELESIS + '\n')
time.sleep(1)
telesis.write('terminal datadump'+'\n') # for cisco it will be 'terminal lenght 0'
telesis.write('\n')
time.sleep(1)
telesis.write('show bridge address-table'+'\n')
time.sleep(0.5)
print('\n')
print ('Getting mac address table, wait 60 seconds.')
time.sleep(60)
bridge_address_telesis = telesis.read_very_eager()
telesis.close()

bridge_list = bridge_address_telesis.split('\r\n')
i = 0
for i in range (len(bridge_list)):
    bridge_list[i] = bridge_list[i].split()

i = 0
interfaces = []
for i in range (len(bridge_list)):
    try:
        if bridge_list[i][2] == 'g1':
            i = i + 1
        if bridge_list[i][2] == '1/g1':
            i = i + 1
        if bridge_list[i][2] == 'ch1':
            i = i + 1
        if bridge_list[i][2] == 'g2':
            i = i + 1
        elif (bridge_list[i][2][0:1] == 'e') or (bridge_list[i][2][1:3] == '/e'):
            interfaces.append(bridge_list[i])
        else:
            i = i + 1
    except IndexError:
        i = i + 1

i = 0
r1 = {interfaces[i][2]:interfaces[i][1] for i in range (len(interfaces))}

i = 0
for interface in r1.keys():
    mac_telesis = r1.get(interface)
    mac_cisco = mac_telesis[0:2] + mac_telesis[3:5] +'.'+ mac_telesis[6:8] + mac_telesis[9:11] +'.'+ mac_telesis[12:14] + mac_telesis[15:]
    r1[interface] = mac_cisco

core = telnetlib.Telnet(IP_CORE)
core.read_until("Username:") #for cisco it will be 'Username'
core.write(USER_CORE + '\n')
core.read_until("Password:")
core.write(PASSWORD_CORE + '\n')
time.sleep(1)
core.write('terminal length 0'+'\n') # for cisco it will be 'terminal length 0'
core.write('\n')
core.write('enable'+'\n')
time.sleep(1)
core.write('cisco' + '\n')
time.sleep(1)
core.write('show ip arp'+'\n')
time.sleep(0.5)
print('\n')
print ('Getting ARP table, wait 120 seconds.')
print('\n')
time.sleep(120)
core_ip_arp = core.read_very_eager()
core.close()

arp_list = core_ip_arp.split()
oui = open('/home/nazarev/python_scripts/vendors/oui_modified2.txt', 'r')
database = oui.read()
database.split('\n')

for interface in r1.keys():
    mac = r1.get(interface)    
    mac_modified = mac.replace('.','')
    mac_modified = mac_modified[0:6].upper()
    try:
        pos_mac = database.index(mac_modified)
        vendor_string = database[pos_mac:pos_mac+(database[pos_mac:].index('\n')-1)].split('\t\t')#add string with mac and vendor name
    except ValueError:
        vendor_string = ['1','Vendor_not_found']    
    try:
        r1[interface] = [mac,arp_list[arp_list.index(mac)-2],vendor_string[1].replace(' ','_')]
    except ValueError:
        r1[interface] = [mac,'No_IP_in_ARP',vendor_string[1].replace(' ','_')]
        
r2 = {}
for interfaces in r1.keys():
    a = r1[interfaces]
    if interfaces.find('/') == -1:
        r2[int(interfaces[1:])] = a
        is_stack = 0
    else:
        is_stack = 1

description = []
if is_stack == 0:
    #отсортирует по возрастанию ключей словаря
    OrderedDict(sorted(r2.items(), key=lambda t: t[0]))
    for interface in r2.keys():        
        string = 'Interface ethernet e' + str(interface) + '\n'
        description.append(string)
        string = 'description ' + r2[interface][1]+'_'+ r2[interface][2]+'\n'
        description.append(string)
        description.append('\n')
    
        
if is_stack == 1:
    for interfaces in r1.keys():
        if len(interfaces) == 4:
            a = interfaces
            a = a[0]+'0'+a[3]
            r2[int(a)]=r1[interfaces]
        if len(interfaces) == 5:
            a = interfaces
            a = a[0]+a[3:]
            r2[int(a)] = r1[interfaces]
    OrderedDict(sorted(r2.items(), key=lambda t: t[0]))
    for interfaces in r2.keys():
        a = str(interfaces)
        if a[1] == '0':
            b = a[0] + '/e'+a[2]
        else:
            b = a[0]+'/e'+a[1:]
        string = 'Interface ethernet ' + b + '\n'
        description.append(string)
        string = 'description ' + r2[interfaces][1]+'_'+ r2[interfaces][2]+'\n'
        description.append(string)
        description.append('\n')

for i in range (len(description)):
    print description[i]

with open('/home/nazarev/python_scripts/description/description_result_new_view.txt', 'w') as description_config:
    description_config.writelines([line for line in description])
