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

data = ''
conn  = None

kilobytes = 1024
megabytes = kilobytes * 1000
chunksize = int(1.4 * megabytes)
readsize = 1024 

#Server function that handles the receiving of files.
def runServer():
        global data
        global conn
        isQUIT = False
        data = '' #data transferred between client and server
        HOST = ''
        PORT = 9001

        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) #allows reuse of address
        s.bind((HOST,PORT))
        s.listen(1)
        conn,addr = s.accept()

        print ("Waiting for client commands...")


        #if the user recieves "bye/Bye," give the option to end the program
        while not isQUIT:
                data = conn.recv(1024)
                if data:
                        command = data.split()[0].upper()
                        if command == 'PWD':
                                conn.sendall(os.getcwd())
                        elif command == 'LIST':
                                conn.sendall(str(len(os.listdir(os.curdir)))) #send the number of items in the directory
                                conn.recv(1024) #wait
                                for fname in os.listdir(os.curdir): #send each file name
                                        conn.sendall(fname)
                                        conn.recv(1024)
                        elif command == 'STOR':
                                receiveFile() #receive file from client to server
                        elif command == 'RETR':
                                sendFile() #send file from server to client
                        elif command == 'QUIT':
                                isQUIT = True


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

def receiveFile():
        global data
        global conn
        partnum = 0
        chunk = ''
        fileName = data.split()[1] #get the name of the file
        numSplits = int(conn.recv(1024)) #receive the number of times the file has been split
        conn.sendall('ack') #continue
        if not os.path.exists('recvDir'):
                os.mkdir('recvDir')                            # make dir, read/write parts
        else:
                for fname in os.listdir('recvDir'):            # delete any existing files
                        os.remove(os.path.join('recvDir', fname))
        for partnum in range(numSplits):
                filename = os.path.join('recvDir', ('part%04d' % partnum)) #define the file
                fileobj  = open(filename, 'wb')
                fileobj.write(conn.recv(1024)) #open the file and write to it the received chunk of data
                fileobj.close() #close the file
        joinFile('recvDir', fileName) #merge the file chunks into one file
        shutil.rmtree('recvDir') #delete the directory after sending the file
        return


def sendFile():
        global data
        global conn
         #SEND SPECIFIED FILE TO THE CLIENT
        fileName = data.split()[1] #get the file name from the string
        if (os.path.isfile(fileName)): #check if file exists before sending it
                numSplits = splitFile(fileName, 'sendDir', 1024)
                conn.sendall(str(numSplits)) #send the number of file splits
                conn.recv(1024) #wait
                parts = os.listdir('sendDir')
                parts.sort()
                for filename in parts:
                        filepath = os.path.join('sendDir', filename)
                        fileobj  = open(filepath, 'rb')
                        while True:
                                filebytes = fileobj.read(readsize)
                                if not filebytes: break
                                conn.sendall(filebytes)
                        fileobj.close()

                # for i in range(numSplits):
                #         s.sendall('part%04d' % i)
                shutil.rmtree('sendDir') #delete the directory after sending the file
        else:
                conn.sendall('ERROR')
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
    while True:                                    # eof=empty string from read
        chunk = input.read(chunksize)              # get next part <= chunksize
        if not chunk: break
        partnum += 1
        filename = os.path.join(todir, ('part%04d' % partnum)) #define the file
        fileobj  = open(filename, 'wb') #open the file
        fileobj.write(chunk) #write the chunk to the file
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
print("Welcome to GCC FTP service")

runServer()

#Terminate
sys.exit()