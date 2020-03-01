import socket
import select
import threading

from Sender import *
from Tracker import *
from AlgoRunner import *


REMOTE_IP = "35.179.45.135"
UDP_ANY_IP = "172.20.179.238"
USERNAME = "Team08"
PASSWORD = "bYrYWPau"

SENDER_PORT = 8666
SENDER_PORT_REMOTE = 8001
TRACKER_PORT = 7666
TRACKER_PORT_REMOTE = 7001

sender_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sender_sock.bind((UDP_ANY_IP, SENDER_PORT))
tracker_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
tracker_sock.bind((UDP_ANY_IP, TRACKER_PORT))

FEEDCODES = ["SP-FUTURE", "ESX-FUTURE"]
SIDES = ["BID", "ASK"]

################################################################################

tracker = Tracker(tracker_sock, REMOTE_IP, TRACKER_PORT_REMOTE)
sender = Sender(sender_sock, REMOTE_IP, SENDER_PORT_REMOTE, USERNAME, PASSWORD)
algo1 = Algo1(tracker, sender)

################################################################################
