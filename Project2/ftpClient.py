# Author:  Ian Spryn, Nate Sprecher
# Course:  COMP 342 Data Communications and Networking
# Date:    24 October 2018
# Description: This program takes an IP address from the user, then connects to another user with
# that IP address. The user is then asked for a chat name. They can exchange messages until one user
# says "bye." Then, the chat communication will end and the other user will be prompted to end the program.

<<<<<<< HEAD
=======
import os
import socket
>>>>>>> f9fac2238a71940752673461ad5f8343823a7341
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
        
        #s.sendall(userName) #send username to other user


        #run as long as the user does not type "Bye/bye" or received "Bye/bye"
         #if the user recieves "bye/Bye," give the option to end the program
        while not userInput != "QUIT":
                userInput = conn.recv(1024)
                if userInput == "LIST":
                        s.sendall(os.listdir())
                if userInput == "PWD":
                        s.sendall(os.getcwd())
                if userInput == "RETR":
                if userInput == "STOR":
        s.close()
        return


<<<<<<< HEAD


=======
>>>>>>> f9fac2238a71940752673461ad5f8343823a7341
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