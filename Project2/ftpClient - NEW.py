# Author:  Ian Spryn, Nate Sprecher
# Course:  COMP 342 Data Communications and Networking
# Date:    24 October 2018
# Description: This program takes an IP address from the user, then connects to another user with
# that IP address. The user is then asked for a chat name. They can exchange messages until one user
# says "bye." Then, the chat communication will end and the other user will be prompted to end the program.

import os
import socket
import time
import sys
import shutil

s = socket.socket()
isQUIT = False #if sent "QUIT"
isSTOR = False
data = ''

kilobytes = 1024
megabytes = kilobytes * 1000
chunksize = int(1.4 * megabytes) 
readsize = 1024



#Client thread that manages the sending of messages. Ends when user types "bye/Bye"
def runClient():
        global s
        global data

        HOST = ''
        PORT = 9001
        command = ''
        commands = ['LIST', 'RETR', 'STOR', 'PWD', 'QUIT']

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


        #run as long as the user does not type "Bye/bye" or received "Bye/bye"
        while not command == "QUIT":
                data = raw_input("Command: ") #get commands from user
                command = data.split()[0].upper()
                if command in commands:
                        if command == 'LIST':
                                s.sendall(data)
                                receiveList() #receive a list of the items in the current directory
                        elif command == 'STOR':
                                s.sendall(data)
                                sendFile() #send file from client to the server
                        elif command == 'RETR':
                                retrieveFile()
                        elif command == 'PWD':
                                s.sendall(data)
                                print(s.recv(1024))
                        else:
                                 s.sendall(data) #if this line is executed, then 'QUIT' has been sent
                else:
                        print("Unknown command")
        s.close()
        return

def receiveList():
        global s
        numFiles = int(s.recv(1024))
        s.sendall('ack') #continue
        for fname in range(numFiles):
                print(s.recv(1024))
                s.sendall('ack') #continue
        return

def sendFile():
        global s
        global data
         #SEND SPECIFIED FILE TO OTHER COMPUTER
        fileName = data.split()[1] #get the file name from the string
        if (os.path.isfile(fileName)): #check if file exists before sending it
                numSplits = splitFile(fileName, 'sendDir', 1024)
                s.sendall(str(numSplits)) #send the number of file splits
                s.recv(1024) #wait
                parts = os.listdir('sendDir')
                parts.sort()
                for filename in parts:
                        filepath = os.path.join('sendDir', filename)
                        fileobj  = open(filepath, 'rb')
                        while True:
                                filebytes = fileobj.read(readsize)
                                if not filebytes: break
                                s.sendall(filebytes)
                        fileobj.close()

                # for i in range(numSplits):
                #         s.sendall('part%04d' % i)
                shutil.rmtree('sendDir') #delete the directory after sending the file
        else:
                print('ERROR: File does not exist')
        return

def retrieveFile():
        global s
        global data
        s.sendall(data) #send the command and the file name
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
        return


#split file, store in given directory
def splitFile(fromfile, todir, chunksize=chunksize): 
    if not os.path.exists(todir):                  # caller handles errors
        os.mkdir(todir)                            # make dir, read/write parts
    else:
        for fname in os.listdir(todir):            # delete any existing files
            os.remove(os.path.join(todir, fname)) 
    partnum = 0
    input = open(fromfile, 'rb')                   # use binary mode on Windows
    while True:                                    # eof=empty string from read
        chunk = input.read(chunksize)              # get next part <= chunksize
        if not chunk: break
        partnum  = partnum+1
        filename = os.path.join(todir, ('part%04d' % partnum))
        fileobj  = open(filename, 'wb')
        fileobj.write(chunk)
        fileobj.close()                            # or simply open(  ).write(  )
    input.close()
    assert partnum <= 9999                         # join sort fails if 5 digits
    return partnum


#function that joins given directory into file
def joinFile(fromdir, tofile):
    output = open(tofile, 'wb')
    parts  = os.listdir(fromdir)
    parts.sort(  )
    for filename in parts:
        filepath = os.path.join(fromdir, filename)
        fileobj  = open(filepath, 'rb')
        while True:
            filebytes = fileobj.read(readsize)
            if not filebytes: break
            output.write(filebytes)
        fileobj.close()
    output.close()
    return


#Start the program by asking the user for an IP address
validIP = False
print("Welcome to GCC FTP client!\n")
#check if valid IP address
while not validIP:
        try:
                ADDRESS = raw_input("Please enter the server's IP address: ")
                socket.inet_aton(ADDRESS) #check if legal IP address
                validIP = True;
        except socket.error:
                pass # Not legal IP address

runClient()

sys.exit()