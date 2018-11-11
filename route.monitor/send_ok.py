#!/usr/bin/env python2.7
# zabbix_sender -z 192.168.1.80 -s route.monitor -k route_changed -o "OK"
import subprocess

x = subprocess.Popen('zabbix_sender -z 192.168.1.80 -s route.monitor -k route_changed -o "OK"', 
                      shell = True, stdout = subprocess.PIPE)

