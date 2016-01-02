#!/usr/bin/python
import sys, os, subprocess, time, string, socket, threading, logging, ConfigParser

## create logging
LOG_FILENAME = 'healthChecker.log'
logging.basicConfig(filename=LOG_FILENAME, level=logging.DEBUG)
logging.basicConfig(filename=LOG_FILENAME, level=logging.INFO)
logging.basicConfig(filename=LOG_FILENAME, level=logging.ERROR)

HealthCheckerIp = sys.argv[1]
NATToHCHotlineListenPort = sys.argv[2]
BufferSize = sys.argv[3]
retryCounter = 5
bindCounter = 2

#############################################################################################################
#   Create hotline receiver socket from NAT to Health Checker
#############################################################################################################

for i in range(0,retryCounter):
    try:
        NATToHCHotlineListenSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    except socket.error as e:
        logging.error('['+time.strftime("%H:%M:%S:")+']'+'Socket:({0}):{1}'.format(e.errno,e.strerror))
        continue
    break

for j in range(0,bindCounter):
    for i in range(0,retryCounter):
        try:
            NATToHCHotlineListenSocket.bind((HealthCheckerIp, int(NATToHCHotlineListenPort)))
        except socket.error as e:
            logging.error('['+time.strftime("%H:%M:%S:")+']'+'Socket:({0}):{1} ('+i+'/5)'.format(e.errno,e.strerror))
            continue
        break

    if i == retryCounter:
        subprocess.call("sudo fuser -k -n tcp " + NATToHCHotlineListenPort, shell=True)
    else
        break

if j == bindCounter:
    sys.exit()

while True:
    try:
        NATToHCHotlineListenSocket.listen(1)
    except socket.error as e:
        logging.error('['+time.strftime("%H:%M:%S:")+']'+'Socket:({0}):{1}'.format(e.errno,e.strerror))
        continue
    break

while True:
    try:
        conn, addr = NATToHCHotlineListenSocket.accept()
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
    if(messageId == 'NH0600'):
        ### NAT is alive. Write the received message to 'NATToHCReply' file
