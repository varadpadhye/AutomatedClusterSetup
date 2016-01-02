#! /usr/bin/python

import sys,subprocess,time,logging,socket, string,ConfigParser

LogFilename = "Monitor.log"
logging.basicConfig(filename=LogFileName, level=logging.INFO)
logging.basicConfig(filename=LogFileName, level=logging.DEBUG)
logging.basicConfig(filename=LogFileName, level=logging.ERROR)

MonitorIP = sys.argv[1]
HCToMONHotlineListenPort = sys.argv[2]
BufferSize = sys.argv[3]
RetryCount = sys.argv[4]

################################################################################
#   Create receiver socket from Healthchecker to Monitor
################################################################################

for i in RetryCount:
    try:
        HCToMONHotlineListenSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    except socket.error as e:
        logging.error('['+time.strftime("%H:%M:%S:")+']' Socket:({0}):{1}.format(e.errno,e.strerror))
        continue
    break

for j in range(0,2):
    for i in RetryCount:
        try:
            HCToMONHotlineListenSocket.bind((MonitorIp,int(HCToMONHotlineListenPort)))
        except socket.error as e:
            logging.error('['+time.strftime("%H:%M:%S:")+']' Socket:({0}):{1} ('+i+'/5).format(e.errno,e.strerror))
            continue
        break
    if i == 5:
        subprocess.call("sudo fuser -k -n tcp"+ HCToMONHotlineListenPort , shell = True)
       
if j == 2:
    sys.exit()

while True:
    try:
        HCtoMONHotlineListenSocket.listen(1)
    except socket.error as e:
        logging.error('['+time.strftime("%H:%M:%S:")+']' Socket:({0}):{1}.format(e.errno,e.strerror))
        continue
    break

while True:
    try:
        conn, addr = HCtoMONHotlineListenSocket.accept()
    except socket.error as e:
        logging.error('['+time.strftime("%H:%M:%S:")+']' Socket:({0}):{1}.format(e.errno,e.strerror))
        continue
    break

logging.info('['+time.strftime("%D-%M-%Y %H:%M:%S"+'] Connection established'+addr)

#############################################################################################################
#   Script that will run infinitely
#############################################################################################################

while True:
    try:
        data = conn.recv(BufferSize)
    except socket.error as e:
        logging.error('['+time.strftime("%H:%M:%S:")+'] Socket:({0}):{1}'.format(e.errno,e.strerror))
        continue
    break

    msgId = string.split(data,':')[0]
    if msgId == 'HM0502':
            #start taking 2nd copy of Healthchecker backup on Monitor
    if msgId == 'HM0501':
            #start taking 3rd copy of NAT backup on Monitor
