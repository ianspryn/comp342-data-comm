# Author:  Ian Spryn, Nate Sprecher
# Course:  COMP 342 Data Communications and Networking
# Date:    12 December 2018
# Description: This HTTP-server allows a client to connect and either access it like a webpage or download a file.

import os
import socket
import time
import sys
import shutil
import math
import datetime

#variables for reading files
kilobytes = 1024
megabytes = kilobytes * 1000
chunksize = int(1.4 * megabytes)

#Server function that handles the receiving of client commands and calls appropriate methods
def runServer():
        HOST = socket.gethostbyname(socket.gethostname())
        PORT = 9001

        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) #allows reuse of address
        s.bind((HOST,PORT))
        s.listen(1)
        conn,addr = s.accept()

        header = conn.recv(1024)
        filePath = header.split()[1]
        sendFile(conn, filePath)
        s.close()
        conn.close()
        return


def sendFile(conn, filePath):
        if filePath == "/": #if no filepath or filename is specified
                filePath = "index.html"
        else:
                filePath = filePath[1:]
        if (os.path.isfile(filePath)): #check if file exists before sending it
                conn.sendall("HTTP/1.1 200 OK\n"
                + "Date: " + str(datetime.datetime.now()) + "\n"
                + "Connection: close\r\n\r\n")
                input = open(filePath, 'rb')
                while True:
                        chunk = input.read(chunksize) #read the data
                        if not chunk: break
                        conn.sendall(chunk)
                input.close()
        else:
                conn.sendall("HTTP/1.0 404 Not Found\n"
                + "Date: " + str(datetime.datetime.now()) + "\n"
                + "Connection: close\r\n\r\n")
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