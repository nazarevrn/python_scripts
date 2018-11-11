#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

import subprocess
import time
from pyzabbix import ZabbixAPI

def iperf_check(ip_pdc):
    global result_iperf, out_result
    p = subprocess.Popen('iperf3 -c ' + ip_pdc + ' -p 5201' + ' -f m -t 30',
                         shell = True, stdout = subprocess.PIPE)
    out_result = p.stdout.read()
    out_result = out_result.split()
    if out_result != ['iperf3:', 'error', '-', 'unable', 'to', 'connect', 'to', 'server:', 'Connection', 'refused']:
        
        send = 'in ' + out_result[out_result.index('sender')-3] + ' '+out_result[out_result.index('sender')-2]
        receive = 'out ' + out_result[out_result.index('receiver')-2] +' '+ out_result[out_result.index('receiver')-1]
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


result_iperf = []


mags = {'mag004':'10.0.24.253', 'mag007':'10.0.48.253', 'mag015':'10.0.112.253'}

for mag in mags.keys():
    iperf_check(mags[mag])
mag = ''    

line = ''
for i in range (len(result_iperf)):
    line = line + str(result_iperf[i])
result_iperf_modi = line.split()    
hosts_speed = []
for mag in mags.keys():
    hosts_speed.append({mag:[{'in':result_iperf_modi[(result_iperf_modi.index(mags[mag])+2)]},
                       {'out':result_iperf_modi[(result_iperf_modi.index(mags[mag])+5)]}]})
    
i = 0
for i in range (len(hosts_speed)):
    zabbix_sender(hosts_speed[i].keys()[0],
                  (hosts_speed[i][hosts_speed[i].keys()[0]][0]).keys()[0],
                  (hosts_speed[i][hosts_speed[i].keys()[0]][0])['in'])
    time.sleep(1)
    zabbix_sender(hosts_speed[i].keys()[0],
                  (hosts_speed[i][hosts_speed[i].keys()[0]][1]).keys()[0],
                  (hosts_speed[i][hosts_speed[i].keys()[0]][1])['out'])
    time.sleep(1)
