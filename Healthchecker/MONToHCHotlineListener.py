#!/usr/bin/python

import socket, subprocess, ConfigParser, time, logging, string

LogFileName = 'healthChecker.log'
logging.basicConfig(filename=LogFileName, level=logging.INFO)
logging.basicConfig(filename=LogFileName, level=logging.DEBUG)
logging.basicConfig(filename=LogFileName, level=logging.ERROR)

HealthCheckerIp = sys.argv[1]
MONToHCHotlineListenPort = sys.argv[2]
BufferSize = sys.argv[3]
retryCounter = 5
bindCounter = 2

#############################################################################################################
#   Create hotline receiver socket from Monitor to Health Checker
#############################################################################################################

for i in range(0,retryCounter):
    try:
        MONToHCHotlineListenSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    except socket.error as e:
        logging.error('['+time.strftime("%H:%M:%S:")+'] Socket:({0}):{1}'.format(e.errno,e.strerror))
        continue
    break

for j in range(0,bindCounter):
    for i in range(0,retryCounter):
        try:
            MONToHCHotlineListenSocket.bind((HealthCheckerIp, int(MONToHCHotlineListenPort)))
        except socket.error as e:
            logging.error('['+time.strftime("%H:%M:%S:")+'] Socket:({0}):{1} ('+i+'/5)'.format(e.errno,e.strerror))
            continue
        break

    if i == retryCounter:
        subprocess.call("sudo fuser -k -n tcp " + MONToHCHotlineListenPort, shell=True)
    else
        break

if j == bindCounter:
    sys.exit()
    # socket can not bind after trying given no of times hence used exit.

while True:
    try:
        MONToHCHotlineListenSocket.listen(1)
    except socket.error as e:
        logging.error('['+time.strftime("%H:%M:%S:")+'] Socket:({0}):{1}'.format(e.errno,e.strerror))
        continue
    break

while True:
    try:
        conn, addr = MONToHCHotlineListenSocket.accept()
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

    if(messageId == 'MH0500'):
        ## do nothing or take backup on NAT
