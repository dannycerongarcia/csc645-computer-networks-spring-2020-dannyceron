import math
# i think this is useful for creating the request messages.
from bitarray import bitarray

class Message:
    """
    this class represents a basic implementation of the peer wire protocol (PWP) used by bitTorret protocol
    to provide reliable communication methods between peers in the same P2P network.
    USAGE:
        message = Message()
        message.init_bitfield()
    """
    #contants:
    X_BITFIELD_LENGTH = b'0000'
    X_PIECE_LENGTH = b'0000'

    def __init__(self):

    """
All non-keepalive messages start with a single byte which gives their type.

The possible values are:

0 - choke
1 - unchoke
2 - interested
3 - not interested
4 - have
5 - bitfield
6 - request
7 - piece
8 - cancel
    """
        # Messages of length zero are kept alive, and ignored.
        # A keep-alive message must be sent to maintain the connection alive if no command
        # have been sent for a given amount of time. This amount of time is generally two minutes.
        self.keep_alive = {'len':b'0000'}

        # the uploader cannot upload more data to the swarm. Causes could be congestion control
        self.choke = {'len':b'0001','id':0}

        # The uploader is ready to upload more data to the swarm
        self.unchoke = {'len':b'0001', 'id':1}

        # The downloader is interested in downloading from the requested peer.
        self.intersted = {'len':b'0001', 'id':2}

        # The downloader is not interested in downloading data from the requested peer.
        self.not_interested = {'len':b'0001','id':3}

        # the payload is a piece that has been sucessfully downloaded and verified via the hash.
        self.have = {'len':b'0005','id':4,'piece_index':None}

        # The payload is a bitfild representing the pieces that have been successfully downloaded.
        # The high bit in the first byte corresponda to piece index 0.
        # Bits that are cleared indicated a missing piece, and set bits indicate a valid and available piece.
        # Spare bits at the end are set to zero
        # [[0,0,0,0,0,0,0,0],[1,1,1,1,1,1,1,1],[1,1,1,1,1,1,1,1]]
        self._bitfield = {'len':b'0013'+self.X_BITFIELD_LENGTH, 'id':5,'bitfield':[]}

        # the request messages is fixed length, and is used to request a block
        # the payload contains the following information.
        # index: interger specify the zero-based piece-index
        # begin: integer specifying the zero-based byets offset within the place
        # length: integer specifying the requested length.
        self.request = {'len':b'0013','id':6,'index':None,'begin':None,'length';None}

        # the request messages is fixed length, and is used to request a block
        # the payload contains the following information.
        # index: interger specify the zero-based piece-index
        # begin: integer specifying the zero-based byets offset within the place
        # block: bloack of data, which is a subset of the piece specofied by index.
        self.piece = {'len':b'0009'+self.X_PIECE_LENGTH,'id':7,'index':None,'begin':None,'block':None}

        # The payload is indentical to that of the request message. it is typically used during "End Game"
        # The "End Game"
        self.cancel = {'len':b'0013','id':8,'index':None,'begin':None,'length':None}

        # the port message is sent by newer version of the mainline that implements a DHT tracker.
        # The listening port is the port this peer's DHT node is listening on.
        # This peer should interested in the local routing table (if DHT tracker is supported)
        self.port = {'index':b'0003',id:9,'listening-port':None}

        # tracker
        self.tracker = {'id':'torret_info_hash':-1,'ip':-1,'port':-1,'upload':-1, 'download':-1,'left':-1,'event':-1}

        def init_bitfield(self,num_pieces):
            """Initialize the bitfield with predefined values
            parameters:
            num_pieces: the number of pieces defined in the .torret file
            """
            size_bitfield = math.ceil(num_pieces/8)
            spare_bits = (8* size_bitfield) - num_pieces
            for i in range(size_bitfield-1):
                piece_bitfield = bitarray(8)
                piece_bitfield.setall(0)
                self._bitfield['bitfield'].append(piece_bitfield)
            spare_piece_bitfield = bitarray(spare_bits)
            spare_piece_bitfield.setall(0)
            self._bitfield['bitfield'].append(spare_piece_bitfield)

        def get_bitfied(self):
            return self._bitfield
        def get_bitfied_pieces(self,piece_index):
            return self._bitfield['bitfield'][piece_index]
        def get_bitfied_block(self,piece_index,block_index):
           return self._bitfield['bitfield'][piece_index][block_index]
        def is_block_mising(self,piece_index,block_index):
            if self._bitfield['bitfield'][piece_index][block_index]:
                return False
            return True
        def is_piece_missing(self,piece_index):
            piece = self._bitfield['bitfield'][piece_index]
            for block_index in range(len(piece_index)):
                if(self.is_block_mising(piece_index,block_index)):
                    return True
                return False
        
        def next_missing_block(self, piece_index):
            piece = self._bitfield['bitfield'][piece_index]
            for block_index in range(len(piece_index)):
                if(self.is_block_mising(piece_index,block_index)):
                    return block_index
                return -1

        def next_missing_piece(self):
            for piece_index in range(len(self._bitfield['bitfield'])):
                if(self.is_block_mising(piece_index)):
                    return piece_index
            return -1

        def set_block_to_completed(self,piece_index,block_index):
            self._bitfield['bitfield'][piece_index][block_index] = True

        def get_have(self,payload):
            piece_index = payload['peice_index']
            self.have['piece_index'] = piece_index
            return self.have
        
        def get_request(self,payload):
            self.request['index'] = payload['index']
            self.request['begin'] = payload['begin']
            self.request['block'] = payload['block']
            return self.request
            
        
        def get_piece(self,payload,len_hex=b'0009'):
            self.piece['index'] = payload['index']
            self.piece['begin'] = payload['begin']
            self.piece['length'] = payload['length']
            if(len_hex >b'0009'):
                self.piece['len'] = len_hex
            return self.piece

        def get_cancel(self,payload):
            self.cancel['index'] = payload['index']
            self.cancel['begin'] = payload['begin']
            self.cancel['length'] = payload['length']
            return self.cancel

        def get_port(self,payload):
            self.port['listen_port'] =  payload['listen_port']
            return self.port
            
        def get_tracker(self,payload):
            self.tracker['torret_info_hash'] = payload['torret_info_hash']
            self.tracker['peer_id'] = payload['peer_id']
            self.tracker['ip'] = payload['ip']
            self.tracker['port'] = payload['port']
            self.tracker['uploaded'] = payload['uploaded']
            self.tracker['downloaded'] = payload['downloaded']
            self.tracker['ledt'] = payload['left']
            self.tracker['event'] = payload['event']
            return self.tracker