#!/usr/bin/python
import sys, os, subprocess, time, string, socket, threading, logging, ConfigParser

## create logging
LOG_FILENAME = 'healthChecker.log'
logging.basicConfig(filename=LOG_FILENAME, level=logging.DEBUG)
logging.basicConfig(filename=LOG_FILENAME, level=logging.INFO)
logging.basicConfig(filename=LOG_FILENAME, level=logging.ERROR)

MONIp = sys.argv[1]
HCToMONHotlineSendPort = sys.argv[2] 
BufferSize = sys.argv[3]
retryCounter= sys.argv[4]

#############################################################################################################
#   Create hotline sender socket between Health Checker and Monitor
#############################################################################################################

for i in range(0,retryCounter):
    try:
        HCToMONHotlineSendSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    except socket.error as e:
        logging.error('['+time.strftime("%H:%M:%S:")+'] Socket:({0}):{1}'.format(e.errno,e.strerror))
        continue
    break

for i in range(0,retryCounter):
    try:
        HCToMONHotlineSendSocket.connect((NatIp, int(HCToMONHotlineSendPort)))
    except socket.error as e:
        logging.error('['+time.strftime("%H:%M:%S:")+'] Socket:({0}):{1}'.format(e.errno,e.strerror))
        continue
    break

logging.info('['+time.strftime("%d_%m_%Y %H:%M:%S")+'] connection established '+addr)

#############################################################################################################
#   Script that will run infinitely
#############################################################################################################

while True:

    #############################################################################################################
    #   Read the messages to send from file 'HCToMONHotlineMsg'
    #############################################################################################################

    while True:
        try:
            filePointer = open("HCToMONHotlineMsg","r")
        except IOError as e:
            logging.error('['+time.strftime("%H:%M:%S")+'] IOError: ({0}):{1}'.format(e.errno,e.strerror))
            continue
        break

    while True:
        try:
            messageList = filePointer.read()
        except IOError as e:
            logging.error('['+time.strftime("%H:%M:%S")+'] IOError: ({0}):{1}'.format(e.errno,e.strerror))
            continue
        break			

    while True:
        try:
            filePointer.close()
        except IOError as e:
            logging.error('['+time.strftime("%H:%M:%S")+'] IOError: ({0}):{1}'.format(e.errno,e.strerror))
            continue
        break

    subprocess.call('echo -n>HCToMONHotlineMsg',shell=True) 

    #############################################################################################################
    #   Send the messages to Monitor one by one
    #############################################################################################################

    i=0
    while i < len(messageList):
        message = messageList[i]

        while True:	
            try:
                HCToMONHotlineSendSocket.send(message)
            except socket.error as e:
                logging.error('['+time.strftime("%H:%M:%S:")+'] Socket:({0}):{1}'.format(e.errno,e.strerror))
                continue
            break
