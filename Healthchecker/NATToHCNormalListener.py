#!/usr/bin/python

import socket, subprocess, ConfigParser, time, logging, string

LogFileName = 'healthChecker.log'
logging.basicConfig(filename=LogFileName, level=logging.INFO)
logging.basicConfig(filename=LogFileName, level=logging.DEBUG)
logging.basicConfig(filename=LogFileName, level=logging.ERROR)

HealthCheckerIp = sys.argv[1]
NATToHCNormalListenPort = sys.argv[2]
BufferSize = sys.argv[3]
retryCounter = 5
bindCounter = 2

#############################################################################################################
#   Create normal receiver socket from NAT to Health Checker
#############################################################################################################

for i in range(0,retryCounter):
    try:
        NATToHCNormalListenSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    except socket.error as e:
        logging.error('['+time.strftime("%H:%M:%S:")+'] Socket:({0}):{1}'.format(e.errno,e.strerror))
        continue
    break

for j in range(0,bindCounter):
    for i in range(0,retryCounter):
        try:
            NATToHCNormalListenSocket.bind((HealthCheckerIp, int(NATToHCNormalListenPort)))
        except socket.error as e:
            logging.error('['+time.strftime("%H:%M:%S:")+'] Socket:({0}):{1} ('+i+'/5)'.format(e.errno,e.strerror))
            continue
        break

    if i == retryCounter:
        subprocess.call("sudo fuser -k -n tcp " + NATToHCNormalListenPort, shell=True)
    else
        break

if j == bindCounter:
    sys.exit()

while True:
    try:
        NATToHCNormalListenSocket.listen(1)
    except socket.error as e:
        logging.error('['+time.strftime("%H:%M:%S:")+'] Socket:({0}):{1}'.format(e.errno,e.strerror))
        continue
    break

while True:
    try:
        conn, addr = NATToHCNormalListenSocket.accept()
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

    if(messageId == 'NH1510'):
        ### start taking backup on minitor now.
    else if(messageId == 'NH1610'):
        ### return lan status
    else if messageId == 'NH1911':
        ### Re-establish socket connections with NAT
