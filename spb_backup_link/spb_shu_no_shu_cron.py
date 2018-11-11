#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-
import paramiko
import time
import datetime

USER = ''
PASSWORD = ''
IP = ''
client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect(hostname=IP, username=USER, password=PASSWORD,
               look_for_keys=False, allow_agent=False)
ssh = client.invoke_shell()
time.sleep(5)
ssh.send('ping 109.236.109.1 source fastEthernet 0/1' + '\n')
time.sleep(15)
result = ssh.recv(5000)
now = datetime.datetime.now()
log = open('/home/nazarev/python_scripts/spb_backup_link/log.txt', 'a')

if result.find('Success rate is 100 percent (5/5)') !=225:
    ssh.send('conf t' + '\n')
    ssh.send('interface fastEthernet 0/1' + '\n')
    time.sleep(0.5)
    ssh.send('shutdown' + '\n')
    time.sleep(2)
    ssh.send('no shutdown' + '\n')
    time.sleep(0.5)
    ssh.send('end' + '\n')
    time.sleep(0.5)
    string_for_write = '!!!Backup interface in SBP has been restarted at ' + now.strftime("%d-%m-%Y %H:%M:%S") + '\n'
else:
    ssh.send('exit' + '\n')
    string_for_write = 'No need to restart backup interface in SBP at ' + now.strftime("%d-%m-%Y %H:%M:%S") + '\n'
ssh.send('exit' + '\n')
log.writelines(string_for_write)
log.close()
log_all = open('/home/nazarev/python_scripts/logs/log.txt', 'a')
log_all.writelines(string_for_write)
log_all.close()
time.sleep(5)


