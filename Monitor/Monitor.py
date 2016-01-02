#! /usr/bin/python
# This script is running on monitor machine.
import os,sys,socket,multiprocessing,ConfigParser,time,logging,subprocess

#create Log
Log_Filename = "monitor.log"
logging.basicConfig(filename=Log_Filename, level=logging.INFO)
logging.basicConfig(filename=Log_Filename, level=logging.DEBUG)
logging.basicConfig(filename=Log_Filename, level=logging.ERROR)
MonitorIP = ""

#Reading from config file
try:
    Config = ConfigParser.ConfigParser()
except ConfigParser.error as e:
    logging.error('['+time.strftime("%H:%M:%S")+']'+'ConfigParser: ({0}): {1}'.format(e.errno, e.strerror))
         
try:    
    Config.read('Monitor.config')

except ConfigParser.error as e:
    logging.error('['+time.strftime("%H:%M:%S")+']'+'ConfigParser: ({0}): {1}'.format(e.errno, e.strerror))

try:
    HCToMONHotlineListenPort = Config.get('MONITOR','MONToHCHotlineListenPort')
except ConfigParser.error as e:
    logging.error('['+time.strftime("%H:%M:%S")+']'+'ConfigParser: ({0}): {1}'.format(e.errno, e.strerror))

try:    
    HCToMONNormalListenPort = Config.get('MONITOR','MONToHCNormalListenPort')
except ConfigParser.error as e:
    logging.error('['+time.strftime("%H:%M:%S")+']'+'ConfigParser: ({0}): {1}'.format(e.errno, e.strerror))

try:    
    MONToHCNormalSendPort = Config.get('MONITOR','MONToHCNormalSendPort')
except ConfigParser.error as e:
    logging.error('['+time.strftime("%H:%M:%S")+']'+'ConfigParser: ({0}): {1}'.format(e.errno, e.strerror))
    
try:    
    MONToHCHotlineSendPort = Config.get('MONITOR','MONToHCHotlineSendPort')
except ConfigParser.error as e:
    logging.error('['+time.strftime("%H:%M:%S")+']'+'ConfigParser: ({0}): {1}'.format(e.errno, e.strerror))

try:
    ORDToMONNormalListenPort = Config.get('MONITOR', 'ORDToMONNormalListenPort')
except ConfigParser.error as e:
    logging.error('['+time.strftime("%H:%M:%S")+']'+'ConfigParser: ({0}): {1}'.format(e.errno, e.strerror))
   
try:
    ORDToMONNormalSendPort = Config.get('MONITOR', 'ORDToMONNormalSendPort')
except ConfigParser.error as e:
    logging.error('['+time.strftime("%H:%M:%S")+']'+'ConfigParser: ({0}): {1}'.format(e.errno, e.strerror))

try:    
    RetryCount = Config.get('COUNTER','RetryCount')
except ConfigParser.error as e:
    logging.error('['+time.strftime("%H:%M:%S")+']'+'ConfigParser: ({0}): {1}'.format(e.errno, e.strerror))
try:    
    BufferSize = Config.get('BUFFER','BufferSize')
except ConfigParser.error as e:
    logging.error('['+time.strftime("%H:%M:%S")+']'+'ConfigParser: ({0}): {1}'.format(e.errno, e.strerror))

try:
    HealthCheckerIp = config.get('HealthChecker','HealthcheckerIp')
except ConfigParser.error as e:
    logging.error('['+time.strftime("%H:%M:%S")+']'+'ConfigParser: ({0}): {1}'.format(e.errno, e.strerror))

HotlineMessage = "CHECK STATE HEALTHCHECKER"

subprocess.call('nice -n 0 python HCToMONHotlineListener.py',MonitorIp,HCToMONHotlineListenPort,BufferSize,RetryCount+'&', shell=True)
subprocess.call('nice -n 0 python MONToHCHotlineSender.py', HealthCheckerIp, MONToHCHotlineSendPort, BUffersize,RetryCount+'&', shell=True)
subprocess.call('python HCToMONNormalListener.py',MonitorIp,HCToMONNormalListenePort,BufferSize,RetryCount+'&', shell=True)
subprocess.call('python MONToHCNormalSender.py',HealthCheckerIP,MONToHCNormalSendPort,BufferSize,RetryCount+'&', shell=True)

while True:
    for i in RetryCount:
        try:
            subprocess.call('ping -c1 HealthCheckerIp', shell=True)
        except CalledProcessError as e:
            logging.error('['+time.strftime("%H:%M:%S")+']'+'ConfigParser: ({0}): {1}'.format(e.errno, e.strerror))
            continue
        break
    
    #send message to all called processes that close all sockets and get exited. 
    #Run HealthChecker script and exit this script.
