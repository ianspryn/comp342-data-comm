# Author:  Ian Spryn, Nate Sprecher
# Course:  COMP 342 Data Communications and Networking
# Date:    24 October 2018
# Description: This program takes an IP address from the user, then connects to another user with
# that IP address. The user is then asked for a chat name. They can exchange messages until one user
# says "bye." Then, the chat communication will end and the other user will be prompted to end the program.

import threading
import socket
import time
import sys

sentBye = False #if client has sent bye
isBye = False #if received bye

#Client thread that manages the sending of messages. Ends when user types "bye/Bye"
def sendFunc():
        global sentBye
        global isBye
        PORT = 9001
        
        connected = False

        print ("Trying to connect...")
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
       
        #run every second until connected                
        while not connected:
                try:
                        s.connect((ADDRESS,PORT))
                        connected = True
                except socket.error:
                        time.sleep(1)

        print ("Connection successful!",ADDRESS)

        userName = raw_input("Please enter your IM Name: ") #get username
        
        s.sendall(userName) #send username to other user


        #run as long as the user does not type "Bye/bye" or received "Bye/bye"
        while not sentBye and not isBye:
                userInput = raw_input(userName + ": ")
                #If user types bye, stop while loop
                if userInput == "Bye" or userInput == "bye":                                                                                   
                        sentBye = True
                s.sendall(userInput) #send user message
        
        s.close()
        return


#Server function that handles the receiving of messages. Ends when it receives "Bye/bye" and user types "y/Yes/yes"
def receiveFunc():
        global sentBye
        global isBye
        HOST = ''
        PORT = 9001

        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) #allows reuse of address
        s.bind((HOST,PORT))
        s.listen(1)
        conn,addr = s.accept()
        #conn.setblocking(0)
        data = ''
        userName = conn.recv(1024)

        #sentBye = False
        isYes = False

        #if the user recieves "bye/Bye," give the option to end the program
        while not isBye:
                #if client hasn't sent bye, then continue the server
                if not sentBye:
                        data = conn.recv(1024)
                        print("\n" + userName + ": " + data)
                        #if "Bye" is received, stop while loop
                        if data == "Bye" or data == "bye":
                                isBye = True
                #if client did send bye, then stop the server and end the program
                else:
                        s.close()
                        conn.close()
                        return

        #if other friend sent "bye", then prompt current user to exit the program
        answer = raw_input(userName + " has ended this conversation. Would you like to exit now?")
        if answer == "Yes" or answer == "yes" or answer == "y":
                        isYes = True
        while not isYes:
                answer = raw_input("But it's all lonely here. How about now?")
                if answer == "Yes" or answer == "yes" or answer == "y":
                        isYes = True
        conn.close()
        return


#Start the program by asking the user for an IP address
validIP = False
print("Welcome to IMChat!\n")
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