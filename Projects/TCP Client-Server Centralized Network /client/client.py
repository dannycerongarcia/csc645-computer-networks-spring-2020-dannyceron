#######################################################################
# File:             client.py
# Author:           Jose Ortiz
# Purpose:          CSC645 Assigment #1 TCP socket programming
# Description:      Template client class. You are free to modify this
#                   file to meet your own needs. Additionally, you are 
#                   free to drop this client class, and add yours instead. 
# Running:          Python 2: python client.py 
#                   Python 3: python3 client.py
#
########################################################################
import socket
import pickle
#adding classes because I dont know how to send the endtire class through the socket
# import menu

# import dill
from threading import Thread
import threading	
import time

class Client(object):
    """
    The client class provides the following functionality:
    1. Connects to a TCP server 
    2. Send serialized data to the server by requests
    3. Retrieves and deserialize data from a TCP server
    """

    def __init__(self):
        """
        Class constractpr
        """
        # Creates the client socket
        # AF_INET refers to the address family ipv4.
        # The SOCK_STREAM means connection oriented TCP protocol.
        self.clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        self.clientid = 0
        self.idKey=""
        self.valid = True
        
    def get_client_id(self):
        return self.clientid

    
    def connect(self, host="127.0.0.1", port=12005):
        """
        TODO: Connects to a server. Implements exception handler if connection is resetted. 
	    Then retrieves the cliend id assigned from server, and sets
        :param host: 
        :param port: 
        :return: VOID
        """
        # pass
        try:
            self.clientSocket.connect((host,port))
            data = self.receive()
            check = 0
            if('clientid' in data):
                self.clientid = data['clientid']
                self.send(self.idKey)
            data = self.receive()
            if('menu' in data):
                    print("menu found")
                    self.send("menu obtained")
            while 1:
                if("closed" in data):
                    break
                # print("in while")
                # data = self.receive()
                # print(data)
                # print("after recieve")
                if not data:
                    break
                # Kinda works
                if('menu' in data):
                    # print("menu found")
                    conf = data['menu']
                    conf.__init__(self)
                    # this part below can be imptemented in the menu class but not sure if i should do it there
                    while(True):
                        # print("in while 2")
                        print(conf.process_user_data())
                        data =None
                        data = self.receive()
                       
                        # print(data)
                        if("listofUsers" in data):
                            print(data["listofUsers"])
                            # input("press enter to continue")
                        print("end of loop")
                        if("200" in data):
                            print(data['200'])
                            # input("press enter to continue")
                        if("myMessages" in data):
                            print(data["myMessages"])
                            # input("press enter to continue")
                        if("room" in data):
                            objectThread = Thread(target=self.inputFun, args=()).start()
                            # self.clientSocket.setblocking(False)
                            while True:
                                # data = self.receive()
                                if "room" in data:
                                    for i in data["room"]:
                                        print(i)
                                # msg =input("Send message: ")
                                # msgData ={"message":msg+"(from: "+self.idKey+")"}
                                self.send(["nothing here"])
                                data = self.receive()
                                # print(data)
                                if(data == None):
                                    data = []
                        if("closed" in data):
                            print(data["closed"])
                            self.close()
                            break
            print("Client ID: ",self.clientid)
        except OSError as msg:
            print("Could not open socket ",msg)
            # self.close()
            self.clientSocket = None
        

        
       
	
    def send(self, data):
        """
        TODO: Serializes and then sends data to server
        :param data:
        :return:
        """
        # pass
        try:
            data = pickle.dumps(data)
            self.clientSocket.send(data)
        except OSError as msg:
            print(msg)
       

    def receive(self, MAX_BUFFER_SIZE=4090):
        """
        TODO: Desearializes the data received by the server
        :param MAX_BUFFER_SIZE: Max allowed allocated memory for this data
        :return: the deserialized data.
        """
        raw_data = None
        try:
            raw_data = self.clientSocket.recv(MAX_BUFFER_SIZE)
            # return dill.loads(raw_data,ignore=True)
            return pickle.loads(raw_data)
        except OSError as msg:
            print(msg)
        
        return raw_data

    def close(self):
        """
        TODO: close the client socket
        :return: VOID
        """
        # pass
        self.clientSocket.close()

    # added this function to run input in a different thread
    def inputFun(self):
        while self.valid:
            time.sleep(.300)
            msg =input("Send message: ")
            if(msg == "exit"):
                msgData ={"message":msg}
            msgData ={"message":msg+"(from: "+self.idKey+")"}
            fun_lock = threading.Lock()
            fun_lock.acquire()
            self.send(msgData)
            fun_lock.release()
            
            

		

if __name__ == '__main__':
    # modified
    ipadd = input("Enter the server IP Address: ")
    port  = input("Enter the server port: ")
    
    # original 
    client = Client()
    client.idKey = input("Your id key (i.e your name): ")
    client.connect()