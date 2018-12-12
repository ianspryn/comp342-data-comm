# Author:  Ian Spryn, Nate Sprecher
# Course:  COMP 342 Data Communications and Networking
# Date:    12 December 2018
# Description: This HTTP-client allows the user to download a webpage or file from the HTTP-server or a public website

import os
import socket
import time
import sys
import shutil
import math

PORT = 0


#Client thread that manages the analyzing of user input and calls appropriate methods to send/receive information
def runClient():
        HOST = ''
        failCount = 0

        #connect to server
        connected = False
        print ("Trying to connect...")
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        while not connected: #run every second until connected
                try:
                        if failCount < 5:
                                #need to set address
                                s.connect((address,PORT))
                                connected = True
                        else:
                                print("Failed to connect to ",address)
                                s.close()
                                sys.exit() #Terminate

                except socket.error:
                        time.sleep(1)
                        failCount += 1
        print ("Connection successful!",address)
        httpRequest = "GET " + filePath + " HTTP/1.1\r\nHost: " + address + "\r\n\r\n"
        fileName = ''
        if filePath == '/':
                fileName = "index2.html" #default name
        else:
                fileName = os.path.basename(filePath) #get name of file at the end of the path
        s.sendall(httpRequest)
        
        output = open(fileName, 'wb') #open file
        result = s.recv(1024)
        result = result.split('\r\n\r\n',1)[1] #ignore the header
        output.write(result)
        while (len(result) > 0): #merge all file chunks into one file
                result = s.recv(1024)
                output.write(result)
        output.close()
        print('File received!')

        s.close()
        return

address = sys.argv[1]
ipHostSplit = address.split(':') #assuming user doesn't type http:// or https://
if len(ipHostSplit) > 1: #assuming user types port
        PORT = int(ipHostSplit[len(ipHostSplit) - 1]) #probably 9001
else:
        PORT = 80
address = ipHostSplit[0]
filePath = ''
if len(sys.argv) > 2: #see if file path is specified
        if not address.endswith('/'):
                filePath += '/'
        filePath += sys.argv[2]
else:
        filePath = '/'#otherwise, set to default

fullPath = address + filePath

runClient()
sys.exit() #Terminate