########################################################################################################################
# Class: Computer Networks
# Date: 02/03/2020
# Lab3: Server support for multiple clients
# Goal: Learning Networking in Python with TCP sockets
# Student Name: Danny Ceron Garcia
# Student ID:918581149
# Student Github Username:dannyceron94
# Lab Instructions: No partial credit will be given. Labs must be completed in class, and must be committed to your
#               personal repository by 9:45 pm.
# Running instructions: This program needs the server to run. The server creates an object of this class.
#
########################################################################################################################
import threading
import socket
from threading import Thread
import pickle


class ClientHandler(object):
    """
    The client handler class receives and process client requests
    and sends responses back to the client linked to this handler.
    """
    def __init__(self, server_instance, clienthandler, addr):
        """
        Class constructor already implemented for you.
        :param server_instance:
        :param clienthandler:
        :param addr:
        """
        self.clientid = addr[1] # the id of the client that owns this handler
        self.server_ip = addr[0]
        self.server = server_instance
        self.clienthandler = clienthandler

    def print_lock(self):
        """
        TODO: create a new print lock
        :return: the lock created
        """
        # your code here.
        print_lock = threading.Lock()
        return print_lock # modify the return to return a the lock created

    def process_client_data(self):

        
        """
        TODO: receives the data from the client
        TODO: prepares the data to be printed in console
        TODO: create a print lock
        TODO: adquire the print lock
        TODO: prints the data in server console
        TODO: release the print lock
        :return: VOID
        """
        while True:
            data_from_client = self.clienthandler.recv(4096)
            pickled_data = pickle.loads(data_from_client)
            if not data_from_client: break
            print_lock = self.print_lock()
            print_lock.acquire()
            print(pickled_data)
            print_lock.release()

