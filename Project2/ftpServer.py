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

sentBye = False #if client has sent bye
isQuit = False #if received bye


#Server function that handles the receiving of messages. Ends when it receives "Bye/bye" and user types "y/Yes/yes"
def server():
        global sentBye
        global isQuit
        HOST = ''
        PORT = 9001
        userInput = ''

        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) #allows reuse of address
        s.bind((HOST,PORT))
        s.listen(1)
        conn,addr = s.accept()
        userName = conn.recv(1024)

        #sentBye = False
        isYes = False

        #if the user recieves "bye/Bye," give the option to end the program
        while not userInput != "QUIT":
                userInput = conn.recv(1024)
                if userInput == "LIST":
                if userInput == "PWD":
                        
                if userInput == "LIST":


        print("Connection terminated by the client...")
        s.close()
        conn.close()
        return


#Start the program by asking the user for an IP address
validIP = False
print("Welcome to GCC FTP service!\nWaiting for client commands...\n")
#check if valid IP address
while not validIP:
        try:
                ADDRESS = raw_input("Please enter the other user's IP address: ")
                socket.inet_aton(ADDRESS) #check if legal IP address
                validIP = True;
        except socket.error:
                pass # Not legal IP address

# Create new threads
receiveThread = threading.Thread(target=receiveFunc)
sendThread = threading.Thread(target=sendFunc)

# Start new Threads
receiveThread.start()
sendThread.start()

#Terminate
sys.exit()