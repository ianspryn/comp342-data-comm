# Author:  Ian Spryn, Nate Sprecher
# Course:  COMP 342 Data Communications and Networking
# Date:    16 November 2018
# Description: This server is an FTP-like application that allows a client (the user) to connect and execute 5 commands
# on the server in total:
# PWD will print the working directory of the server.
# LIST will print all of the items in the directory of the server
# STOR <filename> will store a file from the client on the server's machine if it exists on the client's machine.
# RETR <filename> will retrieve a file from the server if it exists and save it to the client's machine.
# QUIT will terminate the program

import os
import socket
import time
import sys
import shutil
import math

s = socket.socket()
data = ''

#variables for joining and splitting files
kilobytes = 1024
megabytes = kilobytes * 1000
chunksize = int(1.4 * megabytes) 
readsize = 1024

#Client thread that manages the analyzing of user input and calls appropriate methods to send/receive information
def runClient():
        global s
        global data

        HOST = ''
        PORT = 9001
        command = ''
        commands = ['LIST', 'RETR', 'STOR', 'PWD', 'QUIT']

        #connect to server
        connected = False
        print ("Trying to connect...")
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        while not connected: #run every second until connected
                try:
                        s.connect((ADDRESS,PORT))
                        connected = True
                except socket.error:
                        time.sleep(1)
        print ("Connection successful!",ADDRESS)


        #run as long as the user does not type any variation of "QUIT"
        while not command == "QUIT":
                data = raw_input("Command: ") #get input from user
                if data:
                        command = data.split()[0].upper() #get command only from input and convert to uppercase
                        if command in commands:
                                if command == 'LIST':
                                        s.sendall(data)
                                        print(s.recv(1024))
                                        #receiveList() #receive a list of the items in the current directory of the server
                                elif command == 'STOR':
                                        sendFile() #send file from client to the server
                                elif command == 'RETR':
                                        s.sendall(data) #send the command and the file name
                                        receiveFile() #retreive file from server
                                        # print("LIST",s.recv(1024))
                                elif command == 'PWD':
                                        s.sendall(data)
                                        print(s.recv(1024)) #receive the directory of the server
                                else:
                                        s.sendall(data) #if this line is executed, then 'QUIT' has been sent
                        else:
                                print("Unknown command")
        s.close()
        return

#receive a list of the items in the current directory of the sever
def receiveList():
        global s

        numFiles = (s.recv(1024))
        print("VALUE OF NUMFILES", numFiles)
        # numFiles = int(numFiles)

        #numFiles = int(s.recv(1024))

        s.sendall('ack') #continue
        # for fname in range(numFiles):
        #         print(s.recv(1024))
        #         s.sendall('ack') #continue
        return

#send file from client to the server
def sendFile():
        global s
        global data
        fileName = data.split()[1] #get the file name from the string
        if (os.path.isfile(fileName)): #check if file exists before sending the command
                s.sendall(data)
                numSplits = int(math.ceil(float(os.stat(fileName).st_size) / 1024))
                s.recv(1024) #wait
                s.sendall(str(numSplits)) #send the number of file splits
                s.recv(1024) #wait

                input = open(fileName, 'rb')
                while True:
                        chunk = input.read(chunksize) #read the data
                        if not chunk: break
                        s.sendall(chunk)
                input.close()
                print('File sent!')
        else:
                print('ERROR: File does not exist')
        return

#retreive file from server
def receiveFile():
        global s
        global data
        s.sendall('ack')
        numSplits = s.recv(1024)
        s.sendall('ack') #continue
        if 'ERROR' in numSplits: #if we receive 'ERROR', that means the file does not exist
                print('ERROR: File does not exist')
        else:
                fileName = data.split()[1] #get the file name from the previous command
                numSplits = int(numSplits) #receive the number of times the file has been split
                output = open(fileName, 'wb') #open file
                for i in range(numSplits): #merge all file chunks into one file
                        output.write(s.recv(1024))
                output.close()
                print('File received!')
        return

#start the program by asking the user for an IP address
validIP = False
print("Welcome to GCC FTP client!\n")
#check if valid IP address
while not validIP:
        try:
                ADDRESS = raw_input("Please enter the server's IP address: ")
                socket.inet_aton(ADDRESS) #check if legal IP address
                validIP = True;
        except socket.error:
                pass #not legal IP address

runClient()
sys.exit() #Terminate