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

isQUIT = False #if sent "QUIT"
isSTOR = False
data = ''

kilobytes = 1024
megabytes = kilobytes * 1000
chunksize = int(1.4 * megabytes) 
readsize = 1024



#Client thread that manages the sending of messages. Ends when user types "bye/Bye"
def sendFunc():
        global isQUIT
        global isSTOR
        global data

        
        PORT = 9001
        command = ''
        commands = ['LIST', 'RETR', 'STOR', 'PWD', 'QUIT']

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


        #run as long as the user does not type "Bye/bye" or received "Bye/bye"
        while not command == "QUIT":
                data = raw_input("Command: ") #get commands from user
                command = data.split()[0].upper()
                if command in commands:
                        print("I SENT CRAP")
                        s.sendall(data)
                        if "STOR" in command:
                                isSTOR = True
                else:
                        print("Unknown command")
        
        isQUIT = True
        s.close()
        return

#Server function that handles the receiving of files and text.
def receiveFunc():
        global isQUIT
        HOST = ''
        PORT = 9001
        data = ''

        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) #allows reuse of address
        s.bind((HOST,PORT))
        s.listen(1)
        conn,addr = s.accept()

        #sentBye = False
        #isYes = False

        #if the user recieves "bye/Bye," give the option to end the program
        while not isQUIT:
                data = conn.recv(1024)
                #if data == ''
                print(data)


        s.close()
        conn.close()
        return




#split file, store in given directory
def split(fromfile, todir, chunksize=chunksize): 
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
        partnum  = partnum+1
        filename = os.path.join(todir, ('part%04d' % partnum))
        fileobj  = open(filename, 'wb')
        fileobj.write(chunk)
        fileobj.close()                            # or simply open(  ).write(  )
    input.close()
    assert partnum <= 9999                         # join sort fails if 5 digits
    return partnum


#function that joins given directory into file
def join(fromdir, tofile):
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
print("Welcome to GCC FTP client!\n")
#check if valid IP address
while not validIP:
        try:
                ADDRESS = raw_input("Please enter the server's IP address: ")
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