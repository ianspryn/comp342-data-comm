# Author:  Ian Spryn, Nate Sprecher
# Course:  COMP 342 Data Communications and Networking
# Date:    16 November 2018
# Description: This server is an FTP-like application that allows a client (the user) to connect and execute 5 commands
# on the server in total:
# PWD will print the working directory of the server.
# LIST will print all of the items in the directory of the server
# STOR <filename> will store a file from the client on the server's machine if it exists on the client's machine.
# RETR <filename> will retreive a file from the server if it exists and save it to the client's machine.
# QUIT will terminate the program

import os
import socket
import time
import sys
import shutil

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
                command = data.split()[0].upper() #get command only from input and convert to uppercase
                if command in commands:
                        if command == 'LIST':
                                s.sendall(data)
                                receiveList() #receive a list of the items in the current directory of the server
                        elif command == 'STOR':
                                sendFile() #send file from client to the server
                        elif command == 'RETR':
                                s.sendall(data) #send the command and the file name
                                retrieveFile() #retreive file from server
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
        numFiles = int(s.recv(1024))
        s.sendall('ack') #continue
        for fname in range(numFiles):
                print(s.recv(1024))
                s.sendall('ack') #continue
        return

#send file from client to the server
def sendFile():
        global s
        global data
        fileName = data.split()[1] #get the file name from the string
        if (os.path.isfile(fileName)): #check if file exists before sending the command
                s.sendall(data)
                numSplits = splitFile(fileName, 'sendDir', 1024)
                s.sendall(str(numSplits)) #send the number of file splits
                s.recv(1024) #wait
                parts = os.listdir('sendDir')
                #parts = sorted(parts)
                for filename in parts:
                        filepath = os.path.join('sendDir', filename)
                        fileobj  = open(filepath, 'rb') #open the file
                        while True:
                                filebytes = fileobj.read(readsize) #read the data
                                if not filebytes: break
                                s.sendall(filebytes) #send the data
                        fileobj.close()
                shutil.rmtree('sendDir') #delete the directory after sending the file
                print('File sent!')
        else:
                print('ERROR: File does not exist')
        return

#retreive file from server
def retrieveFile():
        global s
        global data
        numSplits = s.recv(1024)
        fileName = data.split()[1] #get the file name from the previous command
        if 'ERROR' in numSplits: #if we receive 'ERROR', that means the file does not exist
                print('ERROR: File does not exist')
        else:
                if not os.path.exists('recvDir'):
                        os.mkdir('recvDir')                            # make dir, read/write parts
                else:
                        for fname in os.listdir('recvDir'):            # delete any existing files
                                os.remove(os.path.join('recvDir', fname))
                numSplits = int(numSplits) #convert string to int
                s.sendall('ack') #continue #continue
                for partnum in range(numSplits):
                        filename = os.path.join('recvDir', ('part%04d' % partnum)) #define the file
                        fileobj  = open(filename, 'wb')
                        fileobj.write(s.recv(1024)) #open the file and write to it the received chunk of data
                        fileobj.close() #close the file
                joinFile('recvDir', fileName) #merge the file chunks into one file
                shutil.rmtree('recvDir') #delete the directory after sending the file
                print('File received!')
        return


#split file, store in given directory
def splitFile(fromfile, todir, chunksize=chunksize): 
        if not os.path.exists(todir):
                os.mkdir(todir) #make directory if it diesn't exist
        else:
                for fname in os.listdir(todir): #delete any existing files
                        os.remove(os.path.join(todir, fname)) 
        partnum = 0
        input = open(fromfile, 'rb')
        while True:
                chunk = input.read(chunksize) #read the data
                if not chunk: break
                partnum  = partnum+1
                filename = os.path.join(todir, ('part%04d' % partnum))
                fileobj  = open(filename, 'wb') #open file
                fileobj.write(chunk) #write data to file
                fileobj.close()
        input.close()
        #assert partnum <= 9999 #join sort fails if 5 digits
        return partnum


#function that joins given directory into file
def joinFile(fromdir, tofile):
        output = open(tofile, 'wb') #open final file
        parts = os.listdir(fromdir) #store list of file chunks
        #parts = sorted(parts)
        for filename in parts:
                filepath = os.path.join(fromdir, filename) #splice the directory and the filename together
                fileobj  = open(filepath, 'rb') #open file part
                while True:
                        filebytes = fileobj.read(readsize) #read chunk
                        if not filebytes: break
                        output.write(filebytes) #write to final file
                fileobj.close()
        output.close()
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