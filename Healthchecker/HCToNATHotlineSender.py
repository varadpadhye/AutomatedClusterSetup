#!/usr/bin/python
import sys, os, subprocess, time, string, socket, threading, logging, ConfigParser

## create logging
LOG_FILENAME = 'healthChecker.log'
logging.basicConfig(filename=LOG_FILENAME, level=logging.DEBUG)
logging.basicConfig(filename=LOG_FILENAME, level=logging.INFO)
logging.basicConfig(filename=LOG_FILENAME, level=logging.ERROR)

NatIp = sys.argv[1]
HCToNATHotlineSendPort = sys.argv[2] 
BufferSize = sys.argv[3]
retryCounter = sys.argv[4]
delay = 1
msgIdList = []

#############################################################################################################
#   Create hotline sender socket between Health Checker and NAT
#############################################################################################################

for i in range(0,retryCounter):
    try:
        HCToNATHotlineSendSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    except socket.error as e:
        logging.error('['+time.strftime("%H:%M:%S:")+'] Socket:({0}):{1}'.format(e.errno,e.strerror))
        continue
    break

for i in range(0,retryCounter):
    try:
        HCToNATHotlineSendSocket.connect((NatIp, int(HCToNATHotlineSendPort)))
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
    #   Read the messages to send from file 'HCToNATHotlineMsg'
    #############################################################################################################

    while True:
        try:
            filePointer = open("HCToNATHotlineMsg","r")
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

    subprocess.call('echo -n>HCToNATHotlineMsg',shell=True)

    #############################################################################################################
    #   Send the messages to NAT one by one
    #############################################################################################################

    i=0
    retries = 0
    while i < len(messageList):
        message = messageList[i]
        while True:	
            try:
                HCToNATHotlineSendSocket.send(message[:-1])
            except socket.error as e:
                logging.error('['+time.strftime("%H:%M:%S:")+'] Socket:({0}):{1}'.format(e.errno,e.strerror))
                continue
            break

        time.sleep(delay)
            
        #############################################################################################################
        #   Check for the reply of the sent message in file 'ORDToHCHotlineReply'
        #############################################################################################################

        while True:
            try:
                filePointer = open("NATToHCHotlineReply","r")
            except IOError as e:
                logging.error('['+time.strftime("%H:%M:%S")+'] IOError: ({0}):{1}'.format(e.errno,e.strerror))
                continue
            break

        while True:
            try:
                replyList = filePointer.read()
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

        subprocess.call('echo -n>NATToHCHotlineReply',shell=True)

        for reply in replyList:
            if string.split(message, ':')[0] == 'HN0800':
                if string.split(reply, ':')[0] == 'NH0600':
                    #NAT is alive. So problem with ping
                    i = i+1
                    break

        retries = retries+1

        if retries == retryCounter:
            #NAT is down. Write that message in 'NATStatus' file
            break
