from const import *
import threading
class Tracker(object):
    def __init__(self, ip_address = "127.0.0.1", port = 12000):
        
        self.port = port
        self.ip_address = ip_address
        self.swarms_list = {}
        self.server = Server(self.ip_address,self.port)

    def add_peer_to_swarm(self, peer_ip, peer_port):
    #    self.swarms_list.update({'ip_address':})
        pass
    
    def thread_tracker(self,client_handler,addr):
        tracker_hand = TrackerHandler(self,self.server,client_handler,addr)
        tracker_hand.run()

    def run(self):
        self.server._listen()
        while True:
            try:
                socket, client_add = self.server.accept()
                Thread(target=self.thread_tracker(socket,client_add))
            except socket.error as socket_exception:
                print(socket_exception)
        


class TrackerHandler():
    def __init__(self, tracker_instance ,server_instance,cleint_hand , addr):
        self.clienthandler = cleint_hand
        self.tracker = tracker_instance
        self.server = server_instance
        self.addr = addr

    def run(self):
        while True:
            data_from_client = self.clienthandler.recv(4096)
            if data_from_client:
                # do stuff
                pass
if __name__ == "__main__":
    tracker = Tracker()
    tracker.run()