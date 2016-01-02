#!/usr/bin/python

import socket, subprocess, ConfigParser, time, logging, string

LogFileName = 'healthChecker.log'
logging.basicConfig(filename=LogFileName, level=logging.INFO)
logging.basicConfig(filename=LogFileName, level=logging.ERROR)
logging.basicConfig(filename=LogFileName, level=logging.DEBUG)

healthCheckerIp = sys.argv[1]
ORDToHCNormalListenPort = sys.argv[2]
BufferSize = sys.argv[3]
retryCounter = 5
bindCounter = 2

#############################################################################################################
#   Create normal receiver socket from Ordinary Machine to Health Checker
#############################################################################################################

for i in range(0,retryCounter):
    try:
        ORDToHCNormalListenSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    except socket.error as e:
        logging.error('['+time.strftime("%H:%M:%S:")+'] Socket:({0}):{1}'.format(e.errno,e.strerror))
        continue
    break

for j in range(0,bindCounter):
    for i in range(0,retryCounter):
        try:
            ORDToHCNormalListenSocket.bind((healthCheckerIp, int(ORDToHCNormalListenPort)))
        except socket.error as e:
            logging.error('['+time.strftime("%H:%M:%S:")+'] Socket:({0}):{1} ('+i+'/5)'.format(e.errno,e.strerror))
            continue
        break

    if i == retryCounter:
        subprocess.call("sudo fuser -k -n tcp " + ORDToHCNormalListenPort, shell=True)
    else
        break

if j == bindCounter:
    sys.exit()

while True:
    try:
        ORDToHCNormalListenSocket.listen(1)
    except socket.error as e:
        logging.error('['+time.strftime("%H:%M:%S:")+'] Socket:({0}):{1}'.format(e.errno,e.strerror))
        continue
    break

while True:
    try:
        conn, addr = ORDToHCNormalListenSocket.accept()
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

    if(messageId == 'OH0811'):
        ### close all sockets and re establish connection with new NAT and restore backup on NAT
    else if(messageId == 'OH0813'):
        ### close all sockets and re establish connection with new Monitor and restore backup on Monitor
