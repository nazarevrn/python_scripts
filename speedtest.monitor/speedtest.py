#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-
import subprocess
import time
from pyzabbix import ZabbixAPI
import signal

def find_pdc_ip(pdc_name):
    global ip_list
    ip_list.append((database[database.index(pdc_name) + 1]))
    
def iperf_check(ip_pdc):
    global result_iperf, out_result
    p = subprocess.Popen('iperf3 -c ' + ip_pdc + ' -p 5201' + ' -f m',
                         shell = True, stdout = subprocess.PIPE)
    out_result = p.stdout.read()
    out_result = out_result.split()
    if out_result[1] != 'error':
        
        send = 'Send ' + out_result[out_result.index('sender')-3] + ' '+out_result[out_result.index('sender')-2]
        receive = 'Receive ' + out_result[out_result.index('receiver')-2] +' '+ out_result[out_result.index('receiver')-1]
        line = ip_pdc + ' ' + send + ' ' + receive + '\n'
        result_iperf.append(line)
    else:
        line = 'Iperf server not runned on host ' + ip_pdc
        result_iperf.append(line)
        
def zabbix_sender(pdc_name_modi, speed_type, speed):
    global out_result_zabbix_sender
    x = subprocess.Popen('zabbix_sender -z 192.168.1.80 -s speedtest.monitor -k '
                         + pdc_name_modi + '.speed.' + speed_type + ' -o '
                         + speed, shell = True, stdout = subprocess.PIPE)
    out_result_zabbix_sender = x.stdout.read()
    out_result_zabbix_sender = out_result_zabbix_sender.split()

z = ZabbixAPI('http://192.168.1.80/zabbix/', user = 'python_scripts',
              password='')
hosts = z.host.get(output=['hostid','host'],
                   selectInterfaces = ['interfaceid','ip'])
database = []
ip_list = []
result_iperf = []
list_of_pdc = []
out_result_zabbix_sender = []
list_pdc_name_modi = []
out_result=''
result_iperf_modi = []
list_zabbix_sender_param = []


hosts_in_network = z.host.get(groupids = 6, output = ['hostid','name'], selectInterfaces = ['interfaceid','ip'])
hosts_in_windows = z.host.get(groupids = 3, output = ['hostid','name'])

i = 0
for i in range (len(hosts_in_network)):
    database.append(str(hosts_in_network[i]['name']))
    database.append(str(hosts_in_network[i]['interfaces'][0]['ip']))


i = 0
j = 0
for i in range (len(hosts_in_network)):
    for j in range (len(hosts_in_windows)):        
        if str(hosts_in_network[i]['name']) == str(hosts_in_windows[j]['name']):
            list_of_pdc.append(str(hosts_in_network[i]['name']))
        else:
            j = j + 1

for pdc_name in list_of_pdc:
    find_pdc_ip(pdc_name)
    
for ip_pdc in ip_list:
    iperf_check(ip_pdc)


i = 0    
for i in range (len(list_of_pdc)):
    if (list_of_pdc[i] == 'idp102p') or (list_of_pdc[i][0:3] == 'mag'):
        list_pdc_name_modi.append(list_of_pdc[i][0:6])
        result_iperf_modi.append(result_iperf[i].split())
        continue
    else:
        list_pdc_name_modi.append(list_of_pdc[i][0:5])
        result_iperf_modi.append(result_iperf[i].split())

i = 0
for i in range (len(list_pdc_name_modi)):
    try:
        if result_iperf_modi[i].index('Send') == 1:
            list_zabbix_sender_param.append(list_pdc_name_modi[i])
            list_zabbix_sender_param.append('in')
            list_zabbix_sender_param.append(result_iperf_modi[i][2])
            list_zabbix_sender_param.append(list_pdc_name_modi[i])
            list_zabbix_sender_param.append('out')
            list_zabbix_sender_param.append(result_iperf_modi[i][5])
    except ValueError:
        i = i + 1

i = 0
j = 0
for i in range (len(list_zabbix_sender_param)/3):
    zabbix_sender(list_zabbix_sender_param[j],
                  list_zabbix_sender_param[j+1],
                  list_zabbix_sender_param[j+2])
    time.sleep(0.5)
    j = j + 3

time.sleep(5)
signal.signal(signal.SIGCHLD, signal.SIG_IGN)
