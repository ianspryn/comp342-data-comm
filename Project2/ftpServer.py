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