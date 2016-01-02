#!/usr/bin/python
import sys, os, subprocess, time, string, socket, threading, logging, ConfigParser

## create logging
LOG_FILENAME = 'healthChecker.log'
logging.basicConfig(filename=LOG_FILENAME, level=logging.DEBUG)
logging.basicConfig(filename=LOG_FILENAME, level=logging.INFO)
logging.basicConfig(filename=LOG_FILENAME, level=logging.ERROR)

sourceIp = sys.argv[1]
sourcePort = sys.argv[2]
BufferSize = sys.argv[3]
retryCounter = sys.argv[4]
targetFile= sys.argv[5]
delay = sys.argv[6]


#############################################################################################################
#   Create hotline receiver socket from NAT to Health Checker
#############################################################################################################

for i in range(0,retryCounter):
    try:
        socketObject = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    except socket.error as e:
        logging.error('['+time.strftime("%H:%M:%S:")+']'+'Socket:({0}):{1}'.format(e.errno,e.strerror))
        continue
    break

for j in range(0,retryCounter):
    for i in range(0,retryCounter):
        try:
            socketObject.bind((sourceIp, int(sourcePort)))
        except socket.error as e:
            logging.error('['+time.strftime("%H:%M:%S:")+']'+'Socket:({0}):{1} ('+i+'/5)'.format(e.errno,e.strerror))
            continue
        break

    if i == retryCounter:
        subprocess.call("sudo fuser -k -n tcp " + sourcePort, shell=True)
    else
        break

if j == retryCounter:
    sys.exit()

while True:
    try:
        socketObject.listen(1)
        conn, addr = socketObject.accept()
    except socket.error as e:
        logging.error('['+time.strftime("%H:%M:%S:")+']'+'Socket:({0}):{1}'.format(e.errno,e.strerror))
        continue
    break

logging.info('['+time.strftime("%d_%m_%Y %H:%M:%S")+']'+'connection established '+addr)

#############################################################################################################
#   Script that will run infinitely
#############################################################################################################

while True:	
    data = conn.recv(BufferSize)
    messageId = string.split(data,':')[0]
    if(messageId == 'NH0500'):
        ### start taking backup on minitor now.

    else if(messageId == 'NH0600'):
        ### NAT is alive. Write the received message to 'NATToHCReply' file

    else if(messageId == 'MH0500'):
        ## do nothing or take backup on NAT

    else if(messageId == 'MH1510'):
        ## do nothing or take backup on NAT(Not decided yet)

    else if(messageId == 'MH1510'):
        ## do nothing or take backup on NAT(Not decided yet)

    else if(messageId == 'NH1510'):
        ### start taking backup on minitor now.

    else if(messageId == 'NH1610'):
        ### return lan status
		
    else if messageId == 'NH1911':
        ### Re-establish socket connections with NAT

    else if(messageId == 'OH0811'):
        ### close all sockets and re establish connection with new NAT and restore backup on NAT

    else if(messageId == 'OH0813'):
        ### close all sockets and re establish connection with new Monitor and restore backup on Monitor
