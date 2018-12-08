# Author:  Ian Spryn, Nate Sprecher
# Course:  COMP 342 Data Communications and Networking
# Date:    16 November 2018
# Description: This server is an FTP-like application that allows a client to connect and execute 5 commands in total:
# PWD will print the working directory of the server.     LIST will print all of the items in the directory of the server
# STOR <filename> will store a file from the client on the server's machine if it exists on the client's machine.
# RETR <filename> will retreive a file from the server if it exists and save it to the client's machine.
# QUIT will terminate the program

import os
import socket
import time
import sys
import shutil

data = ''
conn  = None

#variables for joining and splitting files
kilobytes = 1024
megabytes = kilobytes * 1000
chunksize = int(1.4 * megabytes)
readsize = 1024 

#Server function that handles the receiving of client commands and calls appropriate methods
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
                                        conn.recv(1024) #wait
                        elif command == 'STOR':
                                receiveFile() #receive file from client to server
                        elif command == 'RETR':
                                sendFile() #send file from server to client
                        elif command == 'QUIT':
                                print('Connection terminated by the client...')
                                isQUIT = True
        s.close()
        conn.close()
        return

#receive file from client to server
def receiveFile():
        global data
        global conn
        partnum = 0
        chunk = ''
        fileName = data.split()[1] #get the name of the file
        numSplits = int(conn.recv(1024)) #receive the number of times the file has been split
        conn.sendall('ack') #continue
        if not os.path.exists('recvDir'):
                os.mkdir('recvDir') #make directory if it doesn't exist
        else:
                for fname in os.listdir('recvDir'):
                        os.remove(os.path.join('recvDir', fname)) #delete any existing files in the directory
        for partnum in range(numSplits): #receive each chunk of data
                filename = os.path.join('recvDir', ('part%04d' % partnum)) #define the file to write to
                fileobj  = open(filename, 'wb') #open the file
                fileobj.write(conn.recv(1024)) #write to the file the received chunk of data
                fileobj.close() #close the file
        joinFile('recvDir', fileName) #merge the file chunks into one file with a given filename
        shutil.rmtree('recvDir') #delete the directory after receiving the file
        return

#send file from server to the client
def sendFile():
        global data
        global conn
        fileName = data.split()[1] #get the file name from the string
        if (os.path.isfile(fileName)): #check if file exists before sending it
                numSplits = splitFile(fileName, 'sendDir', 1024)
                conn.sendall(str(numSplits)) #send the number of file splits
                conn.recv(1024) #wait
                parts = os.listdir('sendDir')
                #parts = sorted(parts)
                for filename in parts: #for each chunk of the file, send it in order
                        filepath = os.path.join('sendDir', filename) #get the file chunk
                        fileobj  = open(filepath, 'rb') #open the file chucnk
                        while True:
                                filebytes = fileobj.read(readsize) #read the file chunk
                                if not filebytes: break
                                conn.sendall(filebytes) #send the file chunk
                        fileobj.close()
                shutil.rmtree('sendDir') #delete the directory after sending the file
        else:
                conn.sendall('ERROR') #file does not exist
        return


#function that splits the given file, and stores it into given directory
def splitFile(fromfile, todir, chunksize=chunksize): 
        if not os.path.exists(todir):
                os.mkdir(todir) #make directory if it doesn't exist
        else:
                for fname in os.listdir(todir): #delete any existing files
                        os.remove(os.path.join(todir, fname)) 
        partnum = 0
        input = open(fromfile, 'rb') #open the file
        while True:
                chunk = input.read(chunksize) #get next part <= chunksize
                if not chunk: break
                partnum += 1
                filename = os.path.join(todir, ('part%04d' % partnum)) #define the file
                fileobj  = open(filename, 'wb') #open the file
                fileobj.write(chunk) #write the chunk to the file
                fileobj.close()
        input.close()
        #assert partnum <= 9999 # join sort fails if 5 digits
        return partnum

#function that joins given directory into file
def joinFile(fromdir, tofile):
        output = open(tofile, 'wb') #open file
        parts = os.listdir(fromdir) #get every file directory
        #parts = sorted(parts)
        for filename in parts: #merge all file chunks into one file
                filepath = os.path.join(fromdir, filename) #splice the directory and the filename together
                fileobj  = open(filepath, 'rb')
                while True:
                        filebytes = fileobj.read(readsize) #read file chunk
                        if not filebytes: break
                        output.write(filebytes) #write file chunk to final file
                fileobj.close()
        output.close()
        return

#Start the program by asking the user for an IP address
print("Welcome to GCC FTP service")

runServer()
sys.exit() #Terminate