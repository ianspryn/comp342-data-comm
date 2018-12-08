# Author:  Ian Spryn, Nate Sprecher
# Course:  COMP 342 Data Communications and Networking
# Date:    12 December 2018
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
import datetime

# data = ''
# conn = None

#variables for sending content
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
        HOST = socket.gethostbyname(socket.gethostname())
        PORT = 9001

        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) #allows reuse of address
        s.bind((HOST,PORT))
        s.listen(1)
        conn,addr = s.accept()

        header = conn.recv(1024)
        print("HEADER JUNK")
        print(header)
        filePath = header.split()[1]
        print("\n\n\nFILEPATH")
        print(filePath)
        conn.sendall("HTTP/1.1 200 OK\n"
        + "Date: " + str(datetime.datetime.now()) + "\n"
        + "Connection: close\n\n")

        sendFile(conn, filePath)
        # if filePath == "\\":
        #         sendDefaultIndex()
        # else: #else it's "/someLocation/someFile.type"
        #         sendFile()
        
        s.close()
        conn.close()
        return


def sendDefaultIndex():
        return

def sendFile(conn, filePath):
        if filePath == "/": #if no filepath or filename is specified
                filePath = "index.html"
        if (os.path.isfile(filePath)): #check if file exists before sending it
                # conn.sendall(str(os.stat(fileName).st_size))
                # conn.recv(1024) #wait
                input = open(filePath, 'rb')
                while True:
                        chunk = input.read(chunksize) #read the data
                        if not chunk: break
                        conn.sendall(chunk)
                input.close()
        else:
                input = open("404.html", 'rb')
                while True:
                        chunk = input.read(chunksize) #read the data
                        if not chunk: break
                        conn.sendall(chunk)
                input.close()
        return

#Start the program by asking the user for an IP address
print("Welcome to GCC HTTP service")

runServer()
sys.exit() #Terminate