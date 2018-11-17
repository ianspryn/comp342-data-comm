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
import math

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

                                fileList = ''
                                for fname in os.listdir(os.curdir):
                                        fileList += fname + '\n'
                                conn.sendall(fileList)

                                # conn.sendall(str(len(os.listdir(os.curdir)))) #send the number of items in the directory
                                # conn.recv(1024) #wait
                                # for fname in os.listdir(os.curdir): #send each file name
                                #         conn.sendall(fname)
                                #         conn.recv(1024) #wait
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
        chunk = ''
        fileName = data.split()[1] #get the name of the file
        conn.sendall('ack') #continue
        numSplits = int(conn.recv(1024)) #receive the number of times the file has been split
        conn.sendall('ack') #continue
        output = open(fileName, 'wb') #open file
        for i in range(numSplits): #merge all file chunks into one file
                output.write(conn.recv(1024))
        output.close()
        return



#send file from server to the client
def sendFile():
        global data
        global conn
        fileName = data.split()[1] #get the file name from the string
        if (os.path.isfile(fileName)): #check if file exists before sending it
                numSplits = int(math.ceil(float(os.stat(fileName).st_size) / 1024))
                conn.recv(1024) #wait
                conn.sendall(str(numSplits)) #send the number of file splits
                conn.recv(1024) #wait

                input = open(fileName, 'rb')
                while True:
                        chunk = input.read(chunksize) #read the data
                        if not chunk: break
                        conn.sendall(chunk)
                input.close()
        else:
                conn.recv(1024) #wait
                conn.sendall('ERROR') #file does not exist
                conn.recv(1024) #wait (for consistency with above)
        return


#Start the program by asking the user for an IP address
print("Welcome to GCC FTP service")

runServer()
sys.exit() #Terminate