#! /usr/bin/python

import sys,subprocess,time,logging,string,Socket,ConfigParser

HealthcheckerIp = sys.argv[1]
MONToHCHotlineSendPort = sys.argv[2]
BufferSize = sys.argv[3]
RetryCount = sys.argv[4]
BindRetries = 2

LogFilename = "Monitor.log"
logging.basicConfig(filename=LogFileName, level=logging.INFO)
logging.basicConfig(filename=LogFileName, level=logging.DEBUG)
logging.basicConfig(filename=LogFileName, level=logging.ERROR)

################################################################################
#   Create sender socket from Monitor to Healthchecker
################################################################################

for i in RetryCount:
    try:
        MONToHCHotlineSendSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    except socket.error as e:
        logging.error('['+time.strftime("%H:%M:%S:")+']' Socket:({0}):{1}.format(e.errno,e.strerror))
        continue
    break

for j in range (0, BindRetries):
    for i in RetryCount:
        try:
            MONToHCHotlineSendSocket.Connect((HealthcheckerIp,int(MONToHCHotlineSendPort)))
        except socket.error as e:
            logging.error('['+time.strftime("%H:%M:%S:")+'] Socket:({0}):{1} ('+i+'/5)'.format(e.errno,e.strerror))
            continue
        break
    if i == RetryCount:
        subprocess.call("sudo fuser -k -n tcp"+ MONToHCHotlineSendPort , shell = True)
       
if j == int(BindRetries):
    sys.exit()

logging.info('['+time.strftime("%D-%M-%Y %H:%M:%S"+'] Connection established'+addr)

#############################################################################################################
#   Script that will run infinitely
#############################################################################################################

while True:

    #############################################################################################################
    #   Read the messages to send from file 'MONToHCHotlineMsg'
    #############################################################################################################

    while True:
        try:
            FilePointer = open("MONToHCHotlineMsg","r")
        except IOError as e:
            logging.error('['+time.strftime("%H:%M:%S:")+'] IOError :({0}):{1}'.format(e.errno,e.strerror))
            continue
        break

    while True:
        try:
            messageList = FilePointer.read()
        except IOError as e:
            logging.error('['+time.strftime("%H:%M:%S:")+'] Socket:({0}):{1}'.format(e.errno,e.strerror))
            continue
        break

    while True:
        try:
            FilePointer.close()
        except IOError as e:
            logging.error('['+time.strftime("%H:%M:%S:")+']'+' IOError:({0}):{1}'.format(e.errno,e.strerror))
            continue
        break
    
    subprocess.call('echo -n>MONToHCHotlineMsg',shell=True)
    
    #############################################################################################################
    #   Send the messages to Health Checker one by one
    #############################################################################################################

    i = 0
    while i<len(messageList):
        message = messageList[i]

        try:
            MONToHCNormalSocket.send(message[:-1])
        except socket.error as e:
            logging.error('['+time.strftime("%H:%M:%S:")+'] Socket:({0}):{1}'.format(e.errno,e.strerror))
            continue

        i = i+1
