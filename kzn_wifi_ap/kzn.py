#!/usr/bin/env python2.7
import telnetlib
import time
import getpass
import sys
import datetime

USER = 'nazarev'
PASSWORD = '!'
IP = '10.116.60.11'
t = telnetlib.Telnet(IP)
t.read_until("Username:")
t.write(USER + '\n')
t.read_until("Password:")
t.write(PASSWORD + '\n')
t.write('\n')
time.sleep(1)
t.write('show power inline fastEthernet 0/24'+'\n')
time.sleep(1)
output = t.read_very_eager()
output = output.split()
now = datetime.datetime.now()
log = open('/home/nazarev/python_scripts/kzn_wifi_ap/log.txt', 'a')

if output[25] == 'AIR-LAP1242G-E-K9':
    t.write('exit'+'\n')
    t.close()
    string_for_write = 'No need to reboot AP in KZN at ' + now.strftime("%d-%m-%Y %H:%M:%S") + '\n'
elif output[25] == 'Ieee':
    t.write('conf t'+'\n')
    time.sleep(1)
    t.write('interface fastEthernet 0/24'+'\n')
    time.sleep(1)
    t.write('power inline never'+'\n')
    time.sleep(3)
    t.write('power inline auto'+'\n')
    time.sleep(1)
    t.write('end'+'\n')  
    t.write('exit'+'\n')
    t.close()
    string_for_write = '!!!AP in KZN has been rebooted at ' + now.strftime("%d-%m-%Y %H:%M:%S") + '\n'

log.writelines(string_for_write)
log.close()
log_all = open('/home/nazarev/python_scripts/logs/log.txt', 'a')
log_all.writelines(string_for_write)
log_all.close()


