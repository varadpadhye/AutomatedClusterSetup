#! /usr/bin/python

import sys,suborocess,time,string, ConfigParser,logging

LogFileName = 'healthChecker.log'
logging.basicConfig(filename=LogFileName, level=logging.INFO)
logging.basicConfig(filename=LogFileName, level=logging.DEBUG)
logging.basicConfig(filename=LogFileName, level=logging.ERROR)

NATIp = sys.argv[1]
HCToMONNormalSendPort = sys.argv[2]
BufferSize = sys.argv[3]
retryCounter= sys.argv[4]
waitTime = 1

#############################################################################################################
#   Create normal sender socket between Health Checker and Monitor
#############################################################################################################

for i in range(0,retryCounter):
    try:
        HCToMONNormalSendSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    except socket.error as e:
        logging.error('['+time.strftime("%H:%M:%S:")+']'+'Socket:({0}):{1}'.format(e.errno,e.strerror))
        continue
    break

for i in range(0,retryCounter):
    try:
        HCToMONNormalSendSocket.connect((NATIp, int(HCToMONNormalSendPort)))
    except socket.error as e:
        logging.error('['+time.strftime("%H:%M:%S:")+']'+'Socket:({0}):{1}'.format(e.errno,e.strerror))
        continue
    break

#############################################################################################################
#   Script that will run infinitely
#############################################################################################################

while True:

    #############################################################################################################
    #   Read the messages to send from file 'HCToMONNormalMsg'
    #############################################################################################################

    while True:
        try:
            fileHandler = open("HCToMONNormalMsg", "r")
        except IOError as e:
            time.sleep(waitTime)
            continue
        break

    while True:
        try:
            messageList = fileHandler.read()
        except IOError as e:
            logging.error('['+time.strftime("%H:%M:%S:")+']'+' IOError:({0}):{1}'.format(e.errno,e.strerror))
            continue
        break

    while True:
        try:
            fileHandler.close()
        except IOError as e:
            logging.error('['+time.strftime("%H:%M:%S:")+']'+' IOError:({0}):{1}'.format(e.errno,e.strerror))
            continue
        break

    subprocess.call('echo -n>HCToMONNormalMsg',shell=True)

    #############################################################################################################
    #   Send the messages to Monitor one by one
    #############################################################################################################

    i = 0
    while i<len(messageList):
        message = messageList[i]

        try:
            HCToMONNormalSocket.send(message[:-1])
        except socket.error as e:
            logging.error('['+time.strftime("%H:%M:%S:")+'] Socket:({0}):{1}'.format(e.errno,e.strerror))
            continue

        i = i+1
