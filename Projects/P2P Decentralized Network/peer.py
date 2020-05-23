from const import *
from tracker import Tracker

class Peer(Client, Server):
    # Main program runs the server and the client
    def __init__(self,server_ip_address = '0.0.0.0'):
        Server.__init__(self) # inherist sever methods
        self.server_ip_address = server_ip_address
        self.id = uuid.uuid4()#creates peer id

    def run_server(self):
        # create a thread for the server to then run client at the same time
        try:
            Thread(target=self.run,daemon=True).start()
        except Exception as err:
            print(err)

    def connet_to_peer(self,client_port,peer_ip,peer_port = SERVER_PORT):
        client_object = Client()
        try:
            client_object.bind(DEFAULT_IP,client_port)
            Thread(target=self.client.connect,args=(peer_ip,peer_port)).start()
        except Exception as err:
            print(err)
            client_object.close()
    
    def connect(self, peer_ip_addresses,port=None):
        client_port = CLIENT_MIN_PORT_RANGE
        if port == None:
            default_peer_port = SERVER_PORT
        for peer in peer_ip_addresses:
            if client_port > CLIENT_MAX_PORT_RANGE:
                continue
            if "/" in peer:
                ip_and_port = peer.split("/")
                peer_ip = ip_and_port[0]
                default_peer_port = int(ip_and_port[1])
            if self.connet_to_peer(client_port,peer_ip,default_peer_port):
                client_port += 1

    # def handling_clients(self, client,addr,prot = SERVER_PORT):
    #     try:
    #         t = Thread()
    #     except expression as identifier:
    #         pass
    def get_metainfo(self,path_to_meta):
        # return data from the torrent file
        # with codecs.open(path_to_meta,mode="r",encoding="utf-8", errors="ignore") as torrent_file:
        #     meta_data = torrent_file.read()
        temp_data = self.decode_torrent(path_to_meta)
        # print(temp_data)
        meta_info = {}
        meta_info.update({'filename':temp_data["info"]["name"]})
        # for ip_addr in temp_data['announce']
        # meta_info.update({'ip_address':temp_data['announce'].split(":")})
        meta_info.update({'ip_address':temp_data['announce'].split(":")[0]})
        meta_info.update({'port':(temp_data["announce"]).split(":")[1]})#does not look like the example it supposed to be
        meta_info.update({'piece_len':int(temp_data["info"]["piece length"])})
        meta_info.update({'file_len':int(temp_data["info"]["length"])})
        meta_info.update({'pieces':temp_data["info"]["pieces"]})
        return meta_info

    def decode_torrent(self,torren_path):
        return tp.parse_torrent_file(torren_path)
    def connect_to_tracker(self,ip_addr="127.0.0.1", port = 12000):
        self.connect(ip_addr,port)

        
if __name__ == "__main__":

    peer = Peer()
    peer.run_server()
    path_to_torrent_file = cwd + "/Docs/age.torrent"
    meta_info =peer.get_metainfo(path_to_torrent_file)
    print(meta_info["ip_address"],meta_info["port"])
    peer.connect_to_tracker("127.0.0.1",12000)