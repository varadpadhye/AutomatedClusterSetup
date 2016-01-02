#! /usr/bin/python

import sys,subprocess,time,string,logging,ConfigParser


## create logging
LOG_FILENAME = 'healthChecker.log'
logging.basicConfig(filename=LOG_FILENAME, level=logging.DEBUG)
logging.basicConfig(filename=LOG_FILENAME, level=logging.INFO)
logging.basicConfig(filename=LOG_FILENAME, level=logging.ERROR)

destinationIp = sys.argv[1]
destinationPort = sys.argv[2] 
BufferSize = sys.argv[3]
retryCounter = sys.argv[4]
msgFile = sys.argv[5]
replyFile = sys.argv[6]
delay = sys.argv[7]

#############################################################################################################
#   Create sender socket  
#############################################################################################################

for i in range(0,retryCounter):
    try:
        socketObject = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        socketObject.connect((destinationIp, int(destinationPort)))
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
    #   Read the messages to send from file 
    #############################################################################################################

    while True:
        try:
            filePointer = open(msgFile,"r")
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

    subprocess.call('echo -n>'+msgFile,shell=True)

    #############################################################################################################
    #   Send the messages one by one
    #############################################################################################################

    i=0
    retries = 0
    while i < len(messageList):
        message = messageList[i]

        while True:	
            try:
                socketObject.send(message)
            except socket.error as e:
                logging.error('['+time.strftime("%H:%M:%S:")+'] Socket:({0}):{1}'.format(e.errno,e.strerror))
                continue
            break

        messageId = string.split(message, ':')[0]

        if messageId == 'HN0800' || messageId == 'HO0811' || messageId == 'HO0813':
            time.sleep(delay)
            
            #############################################################################################################
            #   Check for the reply of the sent message in file 'ORDToHCHotlineReply'
            #############################################################################################################

            while True:
                try:
                    filePointer = open(replyFile,"r")
                    replyList = filePointer.read()
                    filePointer.close()
                except IOError as e:
                    logging.error('['+time.strftime("%H:%M:%S")+'] IOError: ({0}):{1}'.format(e.errno,e.strerror))
                    continue
                break

            subprocess.call('echo -n>'+replyFile,shell=True)

            for reply in replyList:
                if messageId == 'HN0800':
                    if string.split(reply, ':')[0] == 'NH0600':
                        #NAT is alive. So problem with ping
                        i = i+1
                        break
                else if messageId == 'HO0811':
                    if string.split(reply, ':')[0] == 'OH0811':
                        #Action to be taken after new NAT is created
                        i = i+1
                        break
                else if messageId == 'HO0813':
                    if string.split(reply, ':')[0] == 'OH0813':
                        #Action to be taken after new monitor is created
                        i = i+1
                        break

            retries = retries+1

            if messageId == 'HN800':
                if retries == retryCounter:
                    #NAT is down. Write that message in 'NATStatus' file
                    break
