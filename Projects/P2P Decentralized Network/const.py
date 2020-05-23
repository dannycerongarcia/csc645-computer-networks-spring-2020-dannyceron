from client import Client
from server import Server
import uuid
from threading import Thread
import os
import codecs
# import bencode.py
import torrent_parser as tp

cwd = os.getcwd()


SERVER_PORT = 5000
CLIENT_MIN_PORT_RANGE = 5001
CLIENT_MAX_PORT_RANGE = 50
DEFAULT_IP = '0.0.0.0'
