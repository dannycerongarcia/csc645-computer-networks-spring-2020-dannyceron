"""
Lab 9: Routing and Handing
Implement the routing and handling functions
"""
from server import Server # assumes server.py is in the root directory.
from const import *

class Peer (Server):

    SERVER_PORT = 5000
    CLIENT_MIN_PORT_RANGE = 5001
    CLIENT_MAX_PORT_RANGE = 5010

    def __init__(self, server_ip_address):
        Server.__init__(server_ip_address, self.SERVER_PORT)

        self.routing_table = Message().get_bitfield()# what data structure will this be?
        self.server_ip_address = server_ip_address
        self.id = uuid.uuid4()
        self.msg = Message()
       



    def run_server(self):
        """
        Already implemented. puts this peer to listen for connections requests from other peers
        :return: VOID
        """
        try:
            run_thread = threading.Thread(target=self.run)
            run_thread.deamon = True
            run_thread.start()
        except Exception as err:
            print(err)


    def _connect_to_peer(self, client_port_to_bind, peer_ip_address,peer_port=PORT):
        """
        TODO: Create a new client object and bind the port given as a
              parameter to that specific client. Then use this client
              to connect to the peer (server) listening in the ip
              address provided as a parameter
        :param client_port_to_bind: the port to bind to a specific client
        :param peer_ip_address: the peer ip address that the client needs to connect to
        :return: VOID
        """
        try:
            # provided the Client class.
            cliet_object = Client()
            cliet_object.bind(ADDRESS,client_port_to_bind)
            connect_thr = threading.Thread(cliet_object.connect_to_server, args=(peer_ip_address,peer_port))
            connect_thr.start()
            return True
        except Exception as err:
            print(err)
            return False
            # pass # handle exceptions here

    def connect(self, peers_ip_addresses):
        """
        TODO: Initialize a temporal variable to the min client port range, then
              For each peer ip address, call the method _connect_to_peer()
              method, and then increment the client´s port range that
              needs to be bind to the next client. Break the loop when the
              port value is greater than the max client port range.

        :param peers: list of peer´s ip addresses in the network
        :return: VOID
        """
        # pass # your code here
        client_port = self.CLIENT_MIN_PORT_RANGE
        default_peer_port =PORT
        for peer in peers_ip_addresses:
            if client_port > self.CLIENT_MAX_PORT_RANGE:
                break
            if "/" in peer:
                ip_and_port = peer.split("/")
                peer_id = ip_and_port[0]
                default_peer_port = int(ip_and_port[1])
            if self._connect_to_peer(client_port,peer_id,default_peer_port):
                client_port += 1

         

    def handling_clients(self, client,addr,port = PORT):
        """
        TODO: handle main services that a specific client provides such as threading the client....
        :param client:
        :return:
        """
        # pass # your code here
        try:
            t = threading.Thread(target=client.connect_to_server,args=(addr,port))
            t.daemon =True
            t.start()
        except Exception as err:
            print(err)

    def routing(self, piece, file_id, swarm_id,client=None):
        """
        TODO: route a piece that was received by this peer, then add that piece to the routing table
        :param piece:
        :param file_id:
        :param swarm_id:
        :return:
        """
        if Client:
            # this is kinda tricky, nothing like the routing tables i read about online 
            
            req = { "data": "data from client"}#request might be different                        
            client.send(req)
            id = client.client_id
            data = client.recieve()
            blcks = data['bitfield'][piece]

            


        else:
            return None
        pass # your code here
