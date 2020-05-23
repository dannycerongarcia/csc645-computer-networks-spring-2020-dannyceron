#######################################################################
# File:             client_handler.py
# Author:           Jose Ortiz
# Purpose:          CSC645 Assigment #1 TCP socket programming
# Description:      Template ClientHandler class. You are free to modify this
#                   file to meet your own needs. Additionally, you are
#                   free to drop this client handler class, and use a version of yours instead.
# Running:          Python 2: python server.py
#                   Python 3: python3 server.py
#                   Note: Must run the server before the client.
########################################################################
import pickle
import menu

# libs for preventing race conditions
import threading
import socket


class ClientHandler(object):
    """
    The ClientHandler class provides methods to meet the functionality and services provided
    by a server. Examples of this are sending the menu options to the client when it connects,
    or processing the data sent by a specific client to the server.
    """
    def __init__(self, server_instance, clientsocket, addr):
        """
        Class constructor already implemented for you
        :param server_instance: normally passed as self from server object
        :param clientsocket: the socket representing the client accepted in server side
        :param addr: addr[0] = <server ip address> and addr[1] = <client id>
        """
        self.server_ip = addr[0]
        self.client_id = addr[1]
        self.server = server_instance
        self.clientsocket = clientsocket
        # self.server.send_client_id(self.clientsocket, self.client_id)
        self.unreaded_messages = []

    def _sendMenu(self):
        """
        Already implemented for you.
        sends the menu options to the client after the handshake between client and server is done.
        :return: VOID
        """
        from menu import Menu
        menu = Menu(None)
        menu_lock = threading.Lock()
        menu_lock.acquire()
        data = {'menu': menu}
        self.server.send(self.clientsocket, data)
        #for debugging
        print("menu sent to "+str(self.client_id))
        print(self.server.receive(self.clientsocket))
        menu_lock.release()


    def process_options(self):
        
        """
        Process the option selected by the user and the data sent by the client related to that
        option. Note that validation of the option selected must be done in client and server.
        In this method, I already implemented the server validation of the option selected.
        :return:
        """
        data = self.server.receive(self.clientsocket)
        if 'option_selected' in data.keys() and 1 <= data['option_selected'] <= 6: # validates a valid option selected
            option = data['option_selected']
            if option == 1:
                self._send_user_list()
            elif option == 2:
                recipient_id = data['recipient_id']
                message = data['message']
                self._save_message(recipient_id, message)
            elif option == 3:
                self._send_messages()
            elif option == 4:
                room_id = data['room_id']
                self._create_chat(room_id)
            elif option == 5:
                room_id = data['room_id']
                self._join_chat(room_id)
            elif option == 6:
                return self._disconnect_from_server()
                
        else:
            print("The option selected is invalid")

    def _send_user_list(self):
        """
        TODO: send the list of users (clients ids) that are connected to this server.
        :return: VOID
        """
        clientList ="" 
        allClients = self.server.clients
        l = len(allClients)
        for index, client in enumerate(allClients):
            if(index+1 == l):
                clientList += allClients[client][0]+":"+str(client)
            else:
                clientList += allClients[client][0]+":"+str(client)+", "
        data = {"listofUsers":"Users in server: "+clientList}
        self.lock_function(self.server.send,self.clientsocket,data)
        #for debugging
        print(data)
        print("list sent")

    def _save_message(self, recipient_id, message):
        """
        TODO: link and save the message received to the correct recipient. handle the error if recipient was not found
        :param recipient_id:
        :param message:
        :return: VOID
        """
        if(recipient_id in self.server.clients and recipient_id in self.server.messages):
            fun_lock = threading.Lock()
            fun_lock.acquire()
            tempArray = self.server.messages[recipient_id]
            tempArray.append(message)
            self.lock_function(self.server.messages.update,({recipient_id:tempArray}))
            print(self.server.messages)
            fun_lock.release()
            data={"200":"Message sent"}
            self.lock_function(self.server.send,self.clientsocket,data)
            
        elif(recipient_id in self.server.clients):
            tempArray =[]
            tempArray.append(message)
            self. lock_function(self.server.messages.update,({recipient_id:tempArray}))
            data={"200":"Message sent"}
            self.lock_function(self.server.send,self.clientsocket,data)
        print(self.server.messages)
        
               

    def _send_messages(self):
        """
        TODO: send all the unreaded messages of this client. if non unread messages found, send an empty list.
        TODO: make sure to delete the messages from list once the client acknowledges that they were read.
        :return: VOID
        """
        data = {"recipient_id":"No new messages"}
        msg =""
        fun_lock = threading.Lock()
        fun_lock.acquire()
        messages = self.server.messages
        
        if self.client_id in messages:
            for key in messages[self.client_id]:
                    msg += key+"\n" 
                
        
        data = {"myMessages":"My messages:\n"+msg}
            
        self.server.send(self.clientsocket, data)
        fun_lock.release()
        # pass

    def _create_chat(self, room_id):
        """
        TODO: Creates a new chat in this server where two or more users can share messages in real time.
        :paramroom_id:
        :return: VOID
        """
        fun_lock = threading.Lock()
        fun_lock.acquire()
        tempArr = []
        tempArr.append("----------------------- Chat Roomv"+room_id+" ------------------------ ")
        tempArr.append("Type 'exit' to close the chat room")
        tempArr.append("Chat room created by: "+self.server.clients[self.client_id][0])
        tempArr.append("Waiting for other users to join....")
        self.server.rooms.update({room_id:tempArr})
        fun_lock.release()
        data={"room":self.server.rooms[room_id]}
        self.lock_function(self.server.send,self.clientsocket,data)
        print("room "+room_id+" created")
        self._join_chat(room_id)
        # pass

    def _join_chat(self, room_id):
        """
        TODO: join a chat in a existing room
        :param room_id:
        :return: VOID
        """
        print(self.client_id, "joined chatroom"+room_id)
        users = []
        # implement race condition here.
        
        try:
            userInput = None
                 
            fun_lock = threading.Lock()
            fun_lock.acquire()
            data = {"groupChat":self.server.rooms[room_id]}
            fun_lock.release()
            clientN={"room":self.server.rooms[room_id]}
            self.lock_function(self.server.send,self.clientsocket,clientN)
            self.server.send(self.clientsocket,data)
            while 1:
                print("in chat while loop")
                userInput = self.server.receive(self.clientsocket)
                if("message" in userInput):
                    if(userInput["message"] =="exit"):
                        # del self.server.clients[self.client_id]
                        data ={"closed":"chat room closed, host has left"}
                        self.server.send(self.clientsocket, data)
                        break
                    fun_lock = threading.Lock()
                    fun_lock.acquire()
                    
                    tempArr = self.server.rooms[room_id]
                    fun_lock.release()
                    tempArr.append(userInput["message"])
                    data ={"room":self.server.rooms[room_id]}
                    self.server.send(self.clientsocket,data)
                
                    
        
        except OSError as msg:
            print(msg)
        # pass

    def delete_client_data(self):
        """
        TODO: delete all the data related to this client from the server.
        :return: VOID
        """
        pass

    def _disconnect_from_server(self):
        """
        TODO: call delete_client_data() method, and then, disconnect this client from the server.
        :return: VOID
        """
        fun_lock = threading.Lock()
        fun_lock.acquire()
        del self.server.clients[self.client_id]
        data ={"closed":"connection ended"}
        self.server.send(self.clientsocket, data)
        fun_lock.release()

        return "kill"
        
        # pass
    
    def process_client_data(self):
        try:
            self._sendMenu()
            while True:
                check = ""
                check = self.process_options()
                if("kill" == check):
                    break
        except OSError as msg:
            # print(msg)
        
            fun_lock = threading.Lock()
            fun_lock.acquire()
            print("trying to update the")
            print(self.client_id)
            del self.server.clients[self.client_id]
            fun_lock.release()
            
        print("client "+str(self.client_id)+ " disconnected")

    def lock_function(self,fun,*args):
        fun_lock = threading.Lock()
        fun_lock.acquire()
        
        fun(*args)
        fun_lock.release()
        