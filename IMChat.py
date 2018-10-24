import threading
import socket
import time

class send (threading.Thread):
        def __init__(self, threadID, name, counter):
                threading.Thread.__init__(self)
                self.threadID = threadID
                self.name = name
        def run(self):
                sendFunct(self.name, self.threadID)

class recieve (threading.Thread):
        def __init__(self, threadID, name, counter):
                threading.Thread.__init__(self)
                self.threadID = threadID
                self.name = name
        def run(self):
                recieveFunc(self.name, self.threadID)


def sendFunct(threadName, threadID):
        HOST='cslnx030.GCC.edu'
        PORT = 9001

        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((HOST,PORT))
        s.sendall('Hello there!')
        data = s.recv(1024)
        print('Recieved: ' + data + "\n")
        s.close()


def recieveFunc(threadName, threadID):
        HOST=''
        PORT = 9001

        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind((HOST,PORT))
        s.listen(1)
        conn,addr = s.accept()
        print 'Connected to',addr
        while 1:
        data = conn.recv(1024)
        if not data:
                break
        print(data + "\n")
        conn.sendall(data)

        
        conn.close()
        
def getIP():
  			print("Welcome to IMChat!\n")
     		userID = raw_input("Please enter the other user's IP address: ")
      	wrongIP = true
        while(wrongIP)
                try:
                        socket.inet_aton(userID)
                        # legal
                except socket.error:
                        # Not legal
                        wrongIP = true