#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-
import telnetlib
import time
import getpass
import sys
import paramiko
#конвертируем mac формата aaaa.bbbb.cccc в aa:aa:bb:bb:cc:cc
def mac_cisco_to_telesis_conv(mac):
    global mac_telesis
    mac_telesis = mac.replace('.', '')
    b = []
    i = 0
    for i in range (0, len(mac_telesis) - 1, 2):
        b.append(mac_telesis[i:(i + 2)])
    mac_telesis = ':'.join(b)
#определяем модель телесиса по баннеру
def type_of_telesis(ip):
    global type_of_telesis_switch
    telesis = telnetlib.Telnet(ip)
    banner = telesis.read_until('#', 1)
    telesis.close()
    if banner.find('User Name') != -1:
        type_of_telesis_switch = 'at8000'
    elif banner.find('login') != -1:
        type_of_telesis_switch = 'fs970'
#определяем модель cisco по баннеру
def type_of_cisco(ip):
    global type_of_cisco_switch
    telesis = telnetlib.Telnet(ip)
    banner = telesis.read_until(':', 1)
    telesis.close()
    if banner.find('User Name') != -1:
        type_of_cisco_switch = 'sf300'
    elif banner.find('Username') != -1:
        type_of_cisco_switch = 'c2900'
 
def find_mac_on_cisco_switch(ip,username,password,mac):
    global cisco_mac_addresses, interface, cisco_number_mac_addresses
    cisco = telnetlib.Telnet(ip)
    cisco.read_until("Username:") #for cisco it will be 'Username'
    cisco.write(username + '\n')
    cisco.read_until("Password:")
    cisco.write(password + '\n')
    time.sleep(0.5)
    cisco.write('terminal length 0'+'\n') # for cisco it will be 'terminal length 0'
    cisco.write('\n')
    time.sleep(0.5)
    cisco.write('enable'+'\n')
    time.sleep(0.5)
    cisco.write('cisco'+'\n')
    time.sleep(0.5)
    cisco.write('show mac address-table address '+ mac +'\n')
    time.sleep(0.5)
    cisco_mac_addresses = cisco.read_very_eager()
    cisco_mac_addresses = cisco_mac_addresses.split()
    cisco_mac_addresses.remove(mac)
    interface = cisco_mac_addresses[cisco_mac_addresses.index(mac) + 2]
    cisco.write('show mac address-table interface '+ interface +'\n')
    time.sleep(0.5)
    cisco_number_mac_addresses = cisco.read_until("#")
    cisco_number_mac_addresses = cisco_number_mac_addresses.split()
    cisco_number_mac_addresses = cisco_number_mac_addresses[cisco_number_mac_addresses.index('criterion:') + 1]
    if int(cisco_number_mac_addresses) < 20:
        print ('Устройство найдено на свиче cisco ' + ip)
        print ('Порт ' + interface)
    cisco.close()
    
def find_mac_on_cisco_switch_sf300(ip,username,password,mac):
    global cisco_mac_addresses, interface, cisco_number_mac_addresses
    cisco = telnetlib.Telnet(ip)
    cisco.read_until("User Name:") #for cisco it will be 'Username'
    cisco.write(username + '\r\n')
    cisco.read_until("Password:")
    cisco.write(password + '\r\n')
    time.sleep(0.5)
    cisco.write('terminal datadump'+'\r\n') # for cisco it will be 'terminal length 0'
    cisco.write('show mac address-table address '+ mac +'\n')
    time.sleep(0.5)
    cisco_mac_addresses = cisco.read_very_eager()
    cisco_mac_addresses = cisco_mac_addresses.split()
    mac_cisco_to_telesis_conv(mac)
    interface = cisco_mac_addresses[cisco_mac_addresses.index(mac_telesis) + 1]
    cisco.write('show mac address-table interface '+ interface +'\n')
    time.sleep(0.5)
    cisco_number_mac_addresses = cisco.read_until("#")
    cisco_number_mac_addresses = cisco_number_mac_addresses.splitlines()
    if len(cisco_number_mac_addresses) < 21:
        print ('Устройство найдено на свиче Cisco ' + ip)
        print('Порт ' + interface)
    cisco.close()


def find_mac_on_telesis_switch_8000(ip,username,password,mac):
    global bridge_address_telesis, telesis_number_mac_addresses, interface
    telesis = telnetlib.Telnet(ip)
    telesis.read_until("User Name:") #for cisco it will be 'Username'
    telesis.write(username + '\n')
    telesis.read_until("Password:")
    telesis.write(password + '\n')
    time.sleep(1)
    telesis.write('terminal datadump'+'\n') # for cisco it will be 'terminal lenght 0'
    telesis.write('\n')
    time.sleep(1)
    telesis.write('show bridge address-table address ' + mac + '\n')
    time.sleep(1)
    bridge_address_telesis = telesis.read_very_eager()
    mac_cisco_to_telesis_conv(mac)
    bridge_address_telesis = bridge_address_telesis.split()
    try:
        interface = bridge_address_telesis[bridge_address_telesis.index(mac_telesis) + 1]
        if interface[0:2] != 'ch':
            telesis.write('show bridge address-table ethernet ' + interface + '\n')
            time.sleep(0.5)
            telesis_number_mac_addresses = telesis.read_until("#")
            telesis_number_mac_addresses = telesis_number_mac_addresses.splitlines()
            if len(telesis_number_mac_addresses) < 12:
                print ('Устройство найдено на свиче Allied telesis ' + ip)
                print('Порт ' + interface)
            telesis.close()
        else:
            telesis.close()
    except ValueError:
        telesis.close()

def find_mac_on_telesis_switch_970(ip,username,password,mac):
    global bridge_address_telesis, telesis_number_mac_addresses, interface
    telesis = telnetlib.Telnet(ip)
    telesis.read_until("login:") #for cisco it will be 'Username'
    telesis.write(username + '\r\n')
    telesis.read_until("Password:")
    telesis.write(password + '\r\n')
    time.sleep(1)
    telesis.write('enable'+'\r\n') # for cisco it will be 'terminal lenght 0'
    telesis.write('terminal length 0'+'\r\n') # for cisco it will be 'terminal length 0'
    telesis.write('\n')
    time.sleep(1)
    telesis.write('show mac address-table include ' + mac + '\r\n')
    time.sleep(3)
    bridge_address_telesis = telesis.read_very_eager()
    #mac_telesis = mac[0:2] + ':' + mac[2:4] + ':' + mac[5:7] + ':' + mac[7:9] + ':' +mac[10:12] + ':' + mac[12:]
    bridge_address_telesis = bridge_address_telesis.split()
    bridge_address_telesis.remove(mac)
    try:
        interface = bridge_address_telesis[bridge_address_telesis.index(mac) - 1]
        telesis.write('show mac address-table interface port' + interface + '\r\n')
        time.sleep(0.5)
        telesis_number_mac_addresses = telesis.read_until("#")
        telesis_number_mac_addresses = telesis_number_mac_addresses.splitlines()
        if len(telesis_number_mac_addresses) < 21:
            print ('Устройство найдено на свиче Allied telesis ' + ip)
            print('Порт ' + interface)
        telesis.close()
    except ValueError:
        telesis.close()
    
        
IP = raw_input("Введите IP искомого девайса: ")
IP_CORE = raw_input("Введите IP корневого свича: ")
LOGIN_CORE = raw_input("Введите логин корневого свича: ")
PASSWORD_CORE = getpass.getpass("Введите пароль корневого свича: ")

core = paramiko.SSHClient()
core.set_missing_host_key_policy(paramiko.AutoAddPolicy())
core.connect(hostname=IP_CORE, username=LOGIN_CORE, password=PASSWORD_CORE,
               look_for_keys=False, allow_agent=False)
ssh = core.invoke_shell()
time.sleep(5)
ssh.send('enable' + '\n')
time.sleep(0.5)
ssh.send('cisco' + '\n')
time.sleep(0.5)
ssh.send('ping ' + IP + '\n')
time.sleep(10)
ssh.send('show ip arp ' + IP + '\n')
time.sleep(2)
arp_output = ssh.recv(5000)
arp_output_list = arp_output.split()
arp_output_list.remove(IP)
arp_output_list.remove(IP)
mac = arp_output_list[arp_output_list.index(IP)+2]
switch_macs_list = []
switch_ip_list = []
if mac.count('.') == 2:
    mac_correct = 1
    ssh.send('show mac address-table address ' + mac + '\n')
    time.sleep(1)
    mac_address_output = ssh.recv(5000)
    mac_address_output_list = mac_address_output.split()
    mac_address_output_list.remove(mac)
    interface = mac_address_output_list[mac_address_output_list.index(mac)+2]
    if interface.find('/') > 0 or interface[0:2] == 'Po':
        interface_correct = 1
        ssh.send('show mac address-table interface ' + interface + ' vlan 60' +'\n')
        time.sleep(2)
        mac_address_interface = ssh.recv(5000)
        mac_address_interface_list = mac_address_interface.split()
        for i in range (len(mac_address_interface_list)):
            if mac_address_interface_list[i].find('.') == 4:
                switch_macs_list.append(mac_address_interface_list[i])
            else:
                continue
        i = 0
        for i in range(len(switch_macs_list)):
            ssh.send('show ip arp ' + switch_macs_list[i] + '\n')
            time.sleep(1)
        switch_ip = ssh.recv(5000)
        switch_ip_list = switch_ip.split('\r\n')
        switch_ip_mac_vendor = {}
        for i in range (2, len(switch_ip_list), 3):
            line = switch_ip_list[i].split()
            switch_ip_mac_vendor[line[1]] = line[3]
        ssh.send('exit' + '\n')
    else:
        interface_correct = 0
        print ('Интерфейс не найден.')
        ssh.send('exit' + '\n')
else:
    mac_correct = 0
    print ('MAC-адрес не найден.')
    ssh.send('exit' + '\n')
i = 0
oui = open('/home/roman/python/venv/PyNEng/labs/vendor&ip_by_mac/oui_modified2.txt', 'r')
database = oui.read()

oui.close()
#создаем словарь. ключ - mac, значение - вендор
b = database.split('\r\n')
x = []
database_dict = {}
for i in range (len(b)-1):
    x = b[i].split('     \t\t')
    database_dict[x[0]] = x[1]

for ip_switch in switch_ip_mac_vendor.keys():
    mac_switch = switch_ip_mac_vendor[ip_switch]
    mac_modi = (mac_switch[0:4] + mac_switch[5:7]).upper()
    try:
        vendor_string = database_dict[mac_modi]
    except KeyError:
        vendor_string = 'Vendor_not_found'
    switch_ip_mac_vendor[ip_switch] = [mac_switch, vendor_string]
    
switches_to_connect = []
for ip_switch in switch_ip_mac_vendor.keys():
    if (switch_ip_mac_vendor[ip_switch][1][0:6] =='Allied') or (switch_ip_mac_vendor[ip_switch][1][0:5] =='Cisco'):
        switches_to_connect.append(ip_switch)
    else:
        continue

for ip_switch in switches_to_connect:
    if switch_ip_mac_vendor[ip_switch][1][0:6] == 'Allied':
        type_of_telesis(ip_switch)
        print ('Ищу на телесисе ' + type_of_telesis_switch + ' ' + ip_switch)
        if type_of_telesis_switch == 'at8000':
            find_mac_on_telesis_switch_8000(ip_switch, 'manager', 'friend', mac)
        elif type_of_telesis_switch == 'fs970':
            find_mac_on_telesis_switch_970(ip_switch, 'manager', 'friend', mac)
    else:
        if switch_ip_mac_vendor[ip_switch][1][0:5] == 'Cisco':
            type_of_cisco(ip_switch)
            print ('Ищу на cisco ' + type_of_cisco_switch + ' ' + ip_switch)
            if type_of_cisco_switch == 'c2900':
                find_mac_on_cisco_switch(ip_switch, LOGIN_CORE, PASSWORD_CORE, mac)
            elif type_of_cisco_switch == 'sf300':
                find_mac_on_cisco_switch_sf300(ip_switch, LOGIN_CORE, PASSWORD_CORE, mac)
        else:
            print ('Вендор устройства не опознан, не знаю, как к нему подключиться. ' + ip_switch)

