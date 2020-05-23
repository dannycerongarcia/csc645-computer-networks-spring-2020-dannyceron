#######################################################################
# File:             server.py
# Author:           Jose Ortiz
# Purpose:          CSC645 Assigment #1 TCP socket programming
# Description:      Template server class. You are free to modify this
#                   file to meet your own needs. Additionally, you are
#                   free to drop this client class, and add yours instead.
# Running:          Python 2: python server.py
#                   Python 3: python3 server.py
#                   Note: Must run the server before the client.
########################################################################

from builtins import object
import socket
from threading import Thread
import pickle
# adding the client and menu classes?
from client_handler import ClientHandler
from menu import Menu
import threading
#stuff i might need to pickle the object
# import dill


class Server(object):

    MAX_NUM_CONN = 10

    def __init__(self, ip_address='127.0.0.1', port=12005):
        """
        Class constructor
        :param ip_address:
        :param port:
        """
        # create an INET, STREAMing socket
        self.serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.clients = {} 
        # TODO: bind the socket to a public host, and a well-known port

        # since there are not variables set for the ipaddress and the port, I am going to do the bind here.3
        try:
            self.serversocket.bind((ip_address,port))
        except OSError as msg:
            print(msg)
        # for the messages
        self.messages = {}
        # for creating room chats
        self.rooms = {}
    # 1st
    def _listen(self):
        """
        Private method that puts the server in listening mode
        If successful, prints the string "Listening at <ip>/<port>"
        i.e "Listening at 127.0.0.1/10000"
        :return: VOID
        """
        #TODO: your code here
        try:
            self.serversocket.listen(self.MAX_NUM_CONN)
            print("server is listening ",self.serversocket.getsockname())
        except OSError as msg:
            print(msg)
        # pass


    def _accept_clients(self):
        """
        Accept new clients
        :return: VOID
        """
        while True:
            try:
                # #TODO: Accept a client
                clientHandler, addr = self.serversocket.accept()
                clientId =  addr[1]
                print(clientId)
                server_lock = threading.Lock()
                server_lock.acquire()
                self.send_client_id(clientHandler,clientId)
                name = self.receive(clientHandler)
                self.clients.update({clientId:[name,"maybe thread instance"]})
                server_lock.release()
               
                #TODO: Create a thread of this client using the client_handler_threaded class
                objectThread = Thread(target=self.client_handler_thread, args=(clientHandler,addr)).start()
               
                
                print(self.clients)
                # pass
            except OSError as msg:
                #TODO: Handle exceptions
                print(msg)
                # pass


    def send(self, clientsocket, data):
        """
        TODO: Serializes the data with pickle, and sends using the accepted client socket.
        :param clientsocket:
        :param data:
        :return:
        """
        serializeData = pickle.dumps(data)
        clientsocket.send(serializeData)
        # pass


    def receive(self, clientsocket, MAX_BUFFER_SIZE=4096):
        """
        TODO: Deserializes the data with pickle
        :param clientsocket:
        :param MAX_BUFFER_SIZE:
        :return: the deserialized data
        """
        dataFromClient = clientsocket.recv(MAX_BUFFER_SIZE)
        return pickle.loads(dataFromClient)

    def send_client_id(self, clientsocket, id):
        """
        Already implemented for you
        :param clientsocket:
        :return:
        """
        clientid = {'clientid': id}
        self.send(clientsocket, clientid)

    def client_handler_thread(self, clientsocket, address):
        """
        Sends the client id assigned to this clientsocket and
        Creates a new ClientHandler object
        See also ClientHandler Class
        :param clientsocket:
        :param address:
        :return: a client handler object.
        """
        # are we not sending data?
        # self.send_client_id(clientsocket,address[1])
        #TODO: create a new client handler object and return it
        chObject = ClientHandler(self,clientsocket,address)
        chObject.process_client_data()
        return chObject


    def run(self):
        """
        Already implemented for you. Runs this client
        :return: VOID
        """
        self._listen()
        self._accept_clients()


if __name__ == '__main__':
    server = Server()
    server.run()


