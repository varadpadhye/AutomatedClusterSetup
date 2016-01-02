#!/usr/bin/python
import subprocess, string, os, socket, time, sys, threading, logging, ConfigParser

## create logging
LOG_FILENAME = 'healthChecker.log'
logging.basicConfig(filename=LOG_FILENAME, level=logging.DEBUG)
logging.basicConfig(filename=LOG_FILENAME, level=logging.INFO)
logging.basicConfig(filename=LOG_FILENAME, level=logging.ERROR)

## read input from config file
Config = ConfigParser.ConfigParser()
Config.read("Health.config")
try:
    NATToHCHotlineListenPort = Config.get('Health','NATToHCHotlineListenPort')
    HCToNATHotlineSendPort = Config.get('Health','HCToNATHotlineSendPort')
    MONToHCHotlineListenPort = Config.get('Health','MONToHCHotlineListenPort')
    HCToMONHotlineSendPort = Config.get('Health','HCToMONHotlineSendPort')
    NATToHCNormalListenPort = Config.get('Health','NATToHCNormalListenPort')
    HCToNATNormalSendPort = Config.get('Health','HCToNATNormalSendPort')
    MONToHCNormalListenPort = Config.get('Health','MONToHCNormalListenPort')
    HCToMONNormalSendPort = Config.get('Health','HCToMONNormalSendPort')
    ORDToHCNormalListenPort = Config.get('Health','ORDToHCNormalListenPort')
    HCToORDNormalSendPort = Config.get('Health','HCToORDNormalSendPort')
    BufferSize = Config.get('Buffer','BufferSize')
    retryCounter = Config.get('counter','retryCounter')
    delay = Config.get('delay','delay')
    NatIp = Config.get('Health','NatIp')
except ConfigParser.error as e:
    logging.error('['+time.strftime("%H:%M:%S:")+'] ConfigParser:({0}):{1}'.format(e.errorno,e.strerror))

prevLive =[]
counter = 0

################## change Calls #####################
try:
		HealthCheckerIp = str(subprocess.check_output("ifconfig eth0 | grep 'inet addr' | awk '{print $2}' |sed -e 's/addr://; ",shell=True))
		subprocess.call(' python ListenerSocket.py '+HealthCheckerIp,NATToHCNormalListenPort,BufferSize,retryConuter+' NATToHCNormalReply '+ delay + ' & ',shell=True)
		subprocess.call(' python ListenerSocket.py '+HealthCheckerIp,MONToHCNormalListenPort,BufferSize,retryCounter+' MONToHCNormalReply '+ delay + ' & ',shell=True)
		subprocess.call(' python ListenerSocket.py '+HealthCheckerIp,ORDToHCNormalListenPort,BufferSize,retryCounter+' ORDToHCNormalReply '+ delay + ' & ',shell=True)
		subprocess.call(' nice -n -9 python ListenerSocket.py '+HealthCheckerIp,NATToHCHotlineListenPort,BufferSize,retryCounter+' NATToHCHotlineReply '+ delay + ' & ',shell=True)
		subprocess.call(' nice -n -9 python ListenerSocket.py '+HealthCheckerIp,MONToHCHotlineListenPort,BufferSize,retryCounter+' MONToHCHotlineReply '+ delay + ' & ',shell=True)
		subprocess.call(' nice -n -9 python SenderSocket.py '+NATIp,HCToNATHotlineSendPort,BufferSize,retryCounter+' HCToNATHotlineMsg NATToHCHotlineReply '+ delay + ' & ',shell=True)
		subprocess.call(' nice -n -9 python SenderSocket.py '+MONIp,HCToMONHotlineSendPort,BufferSize,retryCounter+' HCToMONHotlineMsg MONToHCHotlineReply '+ delay + ' & ',shell=True)
		subprocess.call(' python SenderSocket.py '+NATIp,HCToNATNormalSendPort,BufferSize,retryCounter+' HCToNATNormalMsg NATToHCNormalReply '+ delay + ' & ',shell=True)
		subprocess.call(' python SenderSocket.py '+MONIp,HCToMONNormalSendPort,BufferSize,retryCounter+' HCToMONNormalMsg MONToHCNormalReply '+ delay + ' & ',shell=True)
except CalledProcessError as e:
		logging.error('['+time.strftime("%H:%M:%S:")+'] CalledProcessError:({0}):{1}'.format(e.errorno,e.strerror))





################################################################################################################
#subprocess.call(' python HCToORDNormalSender.py '+ORDIP,HCToORDNormalSendPort,BufferSize,retryCounter+' & ',shell=True)
##################################################################################################################

while True:
    liveMachineFP = open('liveMachineList','w')
    currentLive = subprocess.check_output("fping -a -i 1 -g 192.168.1.0/24 | awk '{print $1}' ",shell=True)
    currentLive = string.split(currentLive)
    newArrivals = list(set(currentLive) - set(prevLive))
    listOfDown = list(set(prevLive) - set(currentLive))
    
    for i in currentLive:
        liveMachineFP.write(i)
        
    liveMachineFP.close()
    
    if NatIp in currentLive:
        prevLive = currentLive
        time.sleep(delay)
        continue
    
    subprocess.call(' python NATStatusChecker.py '+NatIp,retryCounter,BufferSize,HealthCheckerIp,shell=True)
