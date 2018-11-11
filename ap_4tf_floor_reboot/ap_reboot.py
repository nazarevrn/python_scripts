#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

import time
import getpass
import sys
import paramiko
import datetime

ap = paramiko.SSHClient()
ap.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ap.connect(hostname='10.36.54.31', username='', password='',
               look_for_keys=False, allow_agent=False)
ssh = ap.invoke_shell()
time.sleep(5)
ssh.send('show dot11 associations client' + '\n')
time.sleep(1)
client_output = ssh.recv(5000)
client_output = client_output.splitlines()
now = datetime.datetime.now()
log = open('/home/nazarev/python_scripts/ap_4tf_floor_reboot/log.txt', 'a')
if len(client_output) < 11:
    ssh.send('reload' + '\n')
    ssh.send('\r\n')
    string_for_write = '!!!AP on 4th floor has been rebooted at ' + now.strftime("%d-%m-%Y %H:%M:%S") + '\n'

else:
    ssh.send('exit' + '\n')
    string_for_write = 'No need to reboot AP on 4th floor at ' + now.strftime("%d-%m-%Y %H:%M:%S") + '\n'
log.writelines(string_for_write)
log.close()
log_all = open('/home/nazarev/python_scripts/logs/log.txt', 'a')
log_all.writelines(string_for_write)
log_all.close()

