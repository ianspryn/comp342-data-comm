# Author:  Ian Spryn, Nate Sprecher
# Course:  COMP 342 Data Communications and Networking
# Date:    24 October 2018
# Description: This program takes an IP address from the user, then connects to another user with
# that IP address. The user is then asked for a chat name. They can exchange messages until one user
# says "bye." Then, the chat communication will end and the other user will be prompted to end the program.

import os
import threading
import socket
import time
import sys
import shutil

isQUIT = False #if received "QUIT"
isRETR = False
isSTOR = False
isPWD = False
isLIST = False
data = '' #data transferred between client and server

kilobytes = 1024
megabytes = kilobytes * 1000
chunksize = int(1.4 * megabytes)
readsize = 1024 

#Client thread that manages the sending of messages. Ends when user types "bye/Bye"
def sendFunc():
        global isQUIT
        global isRETR
        global isSTOR
        global isPWD
        global isLIST
        global data

        PORT = 9001

        connected = False

        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
       
        #run every second until connected                
        while not connected:
                try:
                        s.connect(('',PORT))
                        connected = True
                except socket.error:
                        time.sleep(1)

        #userName = raw_input("Please enter your IM Name: ") #get username
        
        #s.sendall(userName) #send username to other user


        #run as long as the user does not type "Bye/bye" or received "Bye/bye"
         #if the user recieves "bye/Bye," give the option to end the program
        while not data == "QUIT":
                if isLIST:
                        directoryList = os.listdir()
                        for i in range(len(directoryList)):
                                s.sendall(directoryList[i])
                        isLIST = False
                if isRETR:
                        #SEND SPECIFIED FILE TO OTHER COMPUTER
                        fileName = userInput.split()[1] #get the file name from the string
                        if (os.path.isfile(fileName)): #check if file exists before sending it
                                numSplits = splitFile(fileName, 'sendDir', 1024) #TODO: delete the directory
                                for i in range(numSplits):
                                        s.sendall('part%04d' % i)
                                shutil.rmtree('sendDir')
                        else:
                                s.sendall('File does not exist')
                        isRETR = False
                # if "STOR" in userInput:
                #         isSTOR = True
                #         #TODO give the client the name of the file to be sent
                #         fileName = raw_input()
                if isPWD:
                        s.sendall(os.getcwd())
                        isPWD = False
                                                
                        
                        

                        

        s.close()
        return

#Server function that handles the receiving of files and messages.
def receiveFunc():
        global isQUIT
        global isRETR
        global isSTOR
        global isPWD
        global isLIST
        global data
        HOST = ''
        PORT = 9001

        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) #allows reuse of address
        s.bind((HOST,PORT))
        s.listen(1)
        conn,addr = s.accept()
        #conn.setblocking(0)
        #userName = conn.recv(1024)

        #sentBye = False
        #isYes = False

        print ("Waiting for client commands...")


        #if the user recieves "bye/Bye," give the option to end the program
        print("VALUE OF QUIT: ",isQUIT)
        while not isQUIT:
                data = conn.recv(1024)
                print(data)
                if data:
                        command = data.split()[0].upper()
                        if command == 'PWD':
                                isPWD = True;
                        if command == 'LIST':
                                isLIST = True
                        if command == 'STOR':
                                isSTOR = True
                        if command == 'RETR':
                                isRETR = True


                # #SEND FILE TO THE USER
                # #split() stuff
                # if not os.path.exists('targetDir'):                  
                #         os.mkdir('targetDir')                        
                
                # partnum = 0
                # while true:                                    # eof=empty string from read
                #         chunk = conn.recv(chunksize)             # get next part <= chunksize
                #         if not chunk: break
                #         partnum += 1
                #         directory = os.path.join('targetDir', ('part%04d' % partnum))
                #         fileobj = open(directory, 'wb')
                #         fileobj.write(chunk)
                # fileobj.close()

                        
                # join('targetDir', fileName)
                # shutil.rmtree('targetDir')

        s.close()
        conn.close()
        return

#function that splits the given file, and stores it into given directory
def splitFile(fromfile, todir, chunksize=chunksize): 
    if not os.path.exists(todir):                  # caller handles errors
        os.mkdir(todir)                            # make dir, read/write parts
    else:
        for fname in os.listdir(todir):            # delete any existing files
            os.remove(os.path.join(todir, fname)) 
    partnum = 0
    input = open(fromfile, 'rb')                   # use binary mode on Windows
    while true:                                    # eof=empty string from read
        chunk = input.read(chunksize)              # get next part <= chunksize
        if not chunk: break
        partnum += 1
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
        while true:
            filebytes = fileobj.read(readsize)
            if not filebytes: break
            output.write(filebytes)
        fileobj.close(  )
    output.close(  )

#Start the program by asking the user for an IP address
validIP = False
print("Welcome to GCC FTP service!")


# Create new threads
receiveThread = threading.Thread(target=receiveFunc)
sendThread = threading.Thread(target=sendFunc)

# Start new Threads
receiveThread.start()
sendThread.start()

#Terminate
sys.exit()