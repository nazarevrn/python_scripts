#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

import subprocess
import time
from sys import argv
from pyzabbix import ZabbixAPI
import signal

mib = ['1.3.6.1.2.1.4.24.4.1.4.10.136.72.0.255.255.255.0.0',
       '1.3.6.1.2.1.4.24.4.1.4.192.168.0.0.255.255.0.0.0',
       '1.3.6.1.2.1.4.24.4.1.4.10.36.0.0.255.255.0.0.0']

result_snmpwalk=[]
out_result=''

def send_data_to_host(pdc_name, value):
    x = subprocess.Popen('zabbix_sender -z 192.168.1.80 -s '+pdc_name+
                         ' -k routes_test -o "'+ value + '"',
                         shell = True, stdout = subprocess.PIPE)

def send_data_to_route_check(value):
    x = subprocess.Popen('zabbix_sender -z 192.168.1.80 -s route.monitor -k route_changed -o "'+value+
                         '"', shell = True, stdout = subprocess.PIPE)


def snmpwalk(ip_test_check,mib_check,snmp_comm):
    global result_snmpwalk,out,out_result
    p = subprocess.Popen('snmpwalk -c ' + snmp_comm + ' -v2c ' +
                         ip_test_check + ' ' + mib_check, shell = True,
                         stdout = subprocess.PIPE)
    out_result = p.stdout.read()
    out_result = out_result.split()
    try:
        string_for_write = mib_check[23:mib_check.find('255')-1]+ '-' + out_result[3]
    except IndexError:


        string_for_write = ''
    result_snmpwalk.append(string_for_write)



snmp_comm = 'samson'


#  Connect to zabbix
z = ZabbixAPI('http://192.168.1.80/zabbix/', user = 'python_scripts',
              password='')

# Get hosts in group Route_check in zabbix
hosts_in_route_test = z.host.get(groupids = 104, output = ['hostid','name'],
                   selectInterfaces = ['interfaceid','ip'])

# Making two lists. First - host's ip, second - hostnames in zabbix
i = 0
database = []
database_names = []

for i in range (len(hosts_in_route_test)):
    database.append(str(hosts_in_route_test[i]['interfaces'][0]['ip']))
    database_names.append(str(hosts_in_route_test[i]['name']))


for ip_test_check in database:
    result_snmpwalk.append(ip_test_check)
    for mib_check in mib:
        snmpwalk(ip_test_check,mib_check,snmp_comm)

#Making list of hosts, routes differents from result_snmpwalk[1] 10.136.64.0-10.254.101.1

i = 0
list_zabbix_sender_param = []
line = ''

list_zabbix_sender_param = []


i = 0

# /4 becouse in each host - 4 strings.
# First - host IP
# Second - route to 10.136.72.0
# etc

for i in range ((len(result_snmpwalk))/4):
    list_zabbix_sender_param.append(database_names[database.index(result_snmpwalk[i*4])])
    line = result_snmpwalk[4*i+1] + '\n' + result_snmpwalk[4*i+2] + '\n' + result_snmpwalk[4*i+3]
    list_zabbix_sender_param.append(line)

#Sending data to hosts
i = 0
j = 0
for i in range (len(list_zabbix_sender_param)/2):
    send_data_to_host(list_zabbix_sender_param[j],
                list_zabbix_sender_param[j+1])
    time.sleep(0.5)
    j = j + 2

#Works up top here!

list_zabbix_sender_param_all = []

if result_snmpwalk.count('10.136.72.0-10.254.101.1') > result_snmpwalk.count('10.136.72.0-10.254.102.1'):
    for i in range (0,((len(result_snmpwalk))/4)):
        if result_snmpwalk[result_snmpwalk.index('10.136.72.0-10.254.101.1')] != result_snmpwalk[i*4+1]:
            list_zabbix_sender_param_all.append(database_names[database.index(result_snmpwalk[i*4])])
            line = result_snmpwalk[i*4+1] + '\n' + result_snmpwalk[i*4+2] + '\n'+ result_snmpwalk[i*4+3]
            list_zabbix_sender_param_all.append(line)
        else:
            continue
else:
    for i in range (0,((len(result_snmpwalk))/4)):
        if result_snmpwalk[result_snmpwalk.index('10.136.72.0-10.254.102.1')] != result_snmpwalk[i*4+1]:
            list_zabbix_sender_param_all.append(database_names[database.index(result_snmpwalk[i*4])])
            line = result_snmpwalk[i*4+1] + '\n' + result_snmpwalk[i*4+2] + '\n'+ result_snmpwalk[i*4+3]
            list_zabbix_sender_param_all.append(line)
        else:
            continue

i = 0
j = 0


changed_routes = ''
if len(list_zabbix_sender_param_all) == 0:
    send_data_to_route_check('OK')
else:
    for i in range (len(list_zabbix_sender_param_all)/2):
        changed_routes = changed_routes + str(list_zabbix_sender_param_all[j]) + ' '
        j = j + 2
        send_data_to_route_check(changed_routes)

time.sleep(120)
send_data_to_route_check('OK')


signal.signal(signal.SIGCHLD, signal.SIG_IGN)
