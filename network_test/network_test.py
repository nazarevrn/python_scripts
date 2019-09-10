#!/usr/bin/env python3

import subprocess
import time
import signal
from datetime import datetime

def ping_goole() :
    global packet_loss_percent
    p = subprocess.Popen('ping -c 4 8.8.8.8 ',
                            shell = True, stdout = subprocess.PIPE)
    p.wait()
    out_result = p.stdout.read()

    try:
        splitted = out_result.split(b',')
        packet_loss_data = splitted[2].split()
        packet_loss_percent = packet_loss_data[0]
    except IndexError:
        p = subprocess.Popen('sudo ifconfig enp3s0 up',
                    shell = True, stdout = subprocess.PIPE)
        time.sleep(5)
    #убиваем зомби
    signal.signal(signal.SIGCHLD, signal.SIG_IGN)


ping_goole()

if (packet_loss_percent == b'0%') :
    p = subprocess.Popen('sudo ifconfig enp3s0 down',
                        shell = True, stdout = subprocess.PIPE)
    p.wait()
    time.sleep(1)   
    p = subprocess.Popen('sudo ifconfig enp3s0 up',
                    shell = True, stdout = subprocess.PIPE)
    time.sleep(15)
    ping_goole()

    if (packet_loss_percent == b'0%') :
        #print('All ok!\n')
        now = datetime.now()
        string_for_write = 'Network was restarted at '


else :
    #print('Network not work!\n')
    string_for_write = '!!!Network wasn\'t work at '


log = open('/home/nazarevrn/python_scripts/network_test/log.txt', 'a')
log.writelines(string_for_write + now.strftime("%d-%m-%Y %H:%M:%S") + '\n')
log.close()
#out_result = out_result.split(',')
#print(out_result)
