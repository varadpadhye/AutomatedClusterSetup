#! /usr/bin/python

import sys,suborocess,time,string, ConfigParser,logging

LogFileName = 'healthChecker.log'
logging.basicConfig(filename=LogFileName, level=logging.INFO)
logging.basicConfig(filename=LogFileName, level=logging.DEBUG)
logging.basicConfig(filename=LogFileName, level=logging.ERROR)

NATIp = sys.argv[1]
HCToORDNormalSendPort = sys.argv[2]
BufferSize = sys.argv[3]
retryCounter= sys.argv[4]
waitTime = 1

#############################################################################################################
#   Create normal sender socket between Health Checker and Ordinary Machine
#############################################################################################################

for i in range(0,retryCounter):
    try:
        HCToORDNormalSendSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    except socket.error as e:
        logging.error('['+time.strftime("%H:%M:%S:")+'] Socket:({0}):{1}'.format(e.errno,e.strerror))
        continue
    break

for i in range(0,retryCounter):
    try:
        HCToORDNormalSendSocket.connect((NATIp, int(HCToORDNormalSendPort)))
    except socket.error as e:
        logging.error('['+time.strftime("%H:%M:%S:")+'] Socket:({0}):{1}'.format(e.errno,e.strerror))
        continue
    break

#############################################################################################################
#   Script that will run infinitely
#############################################################################################################

while True:

    #############################################################################################################
    #   Read the messages to send from file 'HCToORDNormalMsg'
    #############################################################################################################

    while True:
        try:
            fileHandler = open("HCToORDNormalMsg", "r")
        except IOError as e:
            time.sleep(waitTime)
            continue
        break
    
    while True:
        try:
            messageList = fileHandler.read()
        except IOError as e:
            logging.error('['+time.strftime("%H:%M:%S:")+'] IOError:({0}):{1}'.format(e.errno,e.strerror))
            continue
        break
    
    while True:
        try:
            fileHandler.close()
        except IOError as e:
            logging.error('['+time.strftime("%H:%M:%S:")+'] IOError:({0}):{1}'.format(e.errno,e.strerror))
            continue
        break
    
    subprocess.call('echo -n>HCToORDNormalMsg',shell=True)      #clear the 'HCToORDNormalMsg' file for future messages
    
    #############################################################################################################
    #   Send the messages to Ordinary machine one by one
    #############################################################################################################

    i = 0
    while i<len(messageList):
        message = messageList[i]
        try:
            HCToORDNormalSocket.send(message[:-1])
        except socket.error as e:
            logging.error('['+time.strftime("%H:%M:%S:")+'] Socket:({0}):{1}'.format(e.errno,e.strerror))
            continue

        time.sleep(waitTime)        #wait for the reply from Ordinary Machine

        #############################################################################################################
        #   Check for the reply of the sent message in file 'ORDToHCNormalReply'
        #############################################################################################################

        try:
            replyFilePtr = open('ORDToHCNormalReply', 'r')
        except IOError as e:
            logging.error('['+time.strftime("%H:%M:%S:")+'] IOError:({0}):{1}'.format(e.errno,e.strerror))
            continue

        try:
            replyList = replyFilePtr.read()
        except IOError as e:
            logging.error('['+time.strftime("%H:%M:%S:")+'] IOError:({0}):{1}'.format(e.errno,e.strerror))
            continue

        try:
            replyFilePtr.close()
        except IOError as e:
            logging.error('['+time.strftime("%H:%M:%S:")+'] IOError:({0}):{1}'.format(e.errno,e.strerror))
            continue

        subprocess.call('echo -n>ORDToHCNormalReply',shell=True)      #clear the 'ORDToHCNormalReply' file for future replies

        for reply in replyList:
            if string.split(message, ':')[0] == 'HO0811':
                if string.split(reply, ':')[0] == 'OH0811':
                    #Action to be taken after new NAT is created
                    i = i+1
                    break
            else if string.split(message, ':')[0] == 'HO0813':
                if string.split(reply, ':')[0] == 'OH0813':
                    #Action to be taken after new monitor is created
                    i = i+1
                    break
