#!/usr/bin/python
import sys, os, subprocess, time, string, socket, threading, logging, ConfigParser

## create logging
LOG_FILENAME = 'healthChecker.log'
logging.basicConfig(filename=LOG_FILENAME, level=logging.DEBUG)
logging.basicConfig(filename=LOG_FILENAME, level=logging.INFO)
logging.basicConfig(filename=LOG_FILENAME, level=logging.ERROR)

currentLive=[]
NatIp = sys.argv[1]
retryCounter = sys.argv[2]
BufferSize = sys.argv[3]
HealthCheckerIp = sys.argv[4]
waitTime = 5

message = 'HN0800:CHECK_NAT_STATUS#UID&@\n'

# read currently live machines ip from file
while True:
    try:
        liveMachineFP = open('liveMachineList','r')
    except IOError as e:
        logging.error('['+time.strftime("%H:%M:%S:")+'] IOError:({0}):{1}'.format(e.errno,e.strerror))
        continue
    break

while True:
    try:
        liveMachine = filePointer.read()
    except IOError as e:
        logging.error('['+time.strftime("%H:%M:%S")+'] IOError: ({0}):{1}'.format(e.errno,e.strerror))
        continue
    break

for line in liveMachine:
    currentlive.append(line)
liveMachineFP.close()

tmp_nat_ip = NatIp[1:len(NatIp)-1]

#########################################################################
#   Check if NAT is not live using PING
#########################################################################

try:
    subprocess.call('ping -c1 '+NatIp+' >/dev/NULL',shell=True)
except CalledProcessError as e:
    logging.error('['+time.strftime("%H:%M:%S:")+'] PING:({0}):{1}'.format(e.errno,e.strerror))

    #########################################################################
    #   retry for retryCounter times
    #########################################################################

    counter = 0
    while counter != retryCounter:
        try:
            subprocess.call('ping -c1 '+NatIp+' >/dev/NULL',shell=True)
        except CalledProcessError as e:
            logging.error('['+time.strftime("%H:%M:%S:")+'] PING:({0}):{1}'.format(e.errno,e.strerror))
            continue
            time.sleep(0.01)
            counter = counter+1
        break

    if counter == retryCounter:
        ## call file that checks NAT status through hotline
        while True:
            try:
                filePointer = open("HCToNATHotlineMsg","a")
            except IOError as e:
                logging.error('['+time.strftime("%H:%M:%S")+'] IOError: ({0}):{1}'.format(e.errno,e.strerror))
                continue
            break

        while True:
            try:
                filePointer.write(message)
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

        time.sleep(waitTime)

        ## read reply of above msg from another file.
        ## if nat down write msg n ip of last host in lan into new file(read by HCToORDNormal sender)

##########################################################################
#   NAT is alive
##########################################################################

logging.info('['+time.strftime("%H:%M:%S")+'] NAT check successful.')
