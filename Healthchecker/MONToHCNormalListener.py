#!/usr/bin/python

import socket, subprocess, ConfigParser, time, logging, string

LogFileName = 'healthChecker.log'
logging.basicConfig(filename=LogFileName, level=logging.INFO)
logging.basicConfig(filename=LogFileName, level=logging.DEBUG)
logging.basicConfig(filename=LogFileName, level=logging.ERROR)

HealthCheckerIp = sys.argv[1]
MONToHCNormalListenPort = sys.argv[2]
BufferSize = sys.argv[3]
retryCounter = 5
bindCounter = 2

#############################################################################################################
#   Create normal receiver socket from Monitor to Health Checker
#############################################################################################################

for i in range(0,retryCounter):
    try:
        MONToHCNormalListenSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    except socket.error as e:
        logging.error('['+time.strftime("%H:%M:%S:")+'] Socket:({0}):{1}'.format(e.errno,e.strerror))
        continue
    break

for j in range(0,bindCounter):
    for i in range(0,retryCounter):
        try:
            MONToHCNormalListenSocket.bind((NormalIp, int(MONToHCNormalListenPort)))
        except socket.error as e:
            logging.error('['+time.strftime("%H:%M:%S:")+'] Socket:({0}):{1} ('+i+'/5)'.format(e.errno,e.strerror))
            continue
        break

    if i == retryCounter:
        subprocess.call("sudo fuser -k -n tcp " + MONToHCNormalListenPort, shell=True)
    else
        break

if j == bindCounter:
    sys.exit()
    # socket can not bind after trying given no of times hence we can't move forward so exit.

while True:
    try:
        MONToHCNormalListenSocket.listen(1)
    except socket.error as e:
        logging.error('['+time.strftime("%H:%M:%S:")+'] Socket:({0}):{1}'.format(e.errno,e.strerror))
        continue
    break

while True:
    try:
        conn, addr = MONToHCNormalListenSocket.accept()
    except socket.error as e:
        logging.error('['+time.strftime("%H:%M:%S:")+'] Socket:({0}):{1}'.format(e.errno,e.strerror))
        continue
    break

logging.info('['+time.strftime("%d_%m_%Y %H:%M:%S")+'] connection established '+addr)

#############################################################################################################
#   Script that will run infinitely
#############################################################################################################

while True:	
    data = conn.recv(BufferSize)
    messageId = string.split(data,':')[0]

    if(messageId == 'MH1510'):
        ## do nothing or take backup on NAT(Not decided yet)
