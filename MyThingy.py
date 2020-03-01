import socket
import select
import threading

from Sender import *
from Tracker import *



REMOTE_IP = "35.179.45.135"
UDP_ANY_IP = "172.20.179.238"
USERNAME = "Team08"
PASSWORD = "bYrYWPau"

EML_UDP_PORT_LOCAL = 8078
EML_UDP_PORT_REMOTE = 8001

eml_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
eml_sock.bind((UDP_ANY_IP, EML_UDP_PORT_LOCAL))

IML_UDP_PORT_LOCAL = 7078
IML_UDP_PORT_REMOTE = 7001

iml_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
iml_sock.bind((UDP_ANY_IP, IML_UDP_PORT_LOCAL))

FEEDCODES = ["SP-FUTURE", "ESX-FUTURE"]
SIDES = ["BID", "ASK"]

################################################################################

tracker = Tracker(iml_sock, REMOTE_IP, IML_UDP_PORT_REMOTE)
sender = Sender(eml_sock, REMOTE_IP, EML_UDP_PORT_REMOTE, USERNAME, PASSWORD)

tt = threading.Thread(target=tracker.run)

################################################################################

last_prices = {
        "ESX-FUTURE": {
            "ASK": None,
            "BID": None
            },
        "SP-FUTURE": {
            "ASK": None,
            "BID": None
            }
        }

def algo1():
    N = 100
    m = 4
    fa = []
    fb = []
    while True:
        for feedcode in FEEDCODES:
            cur_price_ASK = tracker.FCHistories[feedcode]["ASK"].price
            if cur_price_ASK != last_prices[feedcode]["ASK"]:
                last_ten_prices_ASK = tracker.FCHistories[feedcode]["ASK"].prices[-12:-2]
                good_price_ASK = min(last_ten_prices_ASK) + ((max(last_ten_prices_ASK) - min(last_ten_prices_ASK)) / m)
                if cur_price_ASK < good_price_ASK:
                    print("buying " + feedcode + str(last_ten_prices_ASK) + ", " + str(cur_price_ASK) + ", " + str(good_price_ASK))
                    sender.send_order(feedcode, "BUY", cur_price_ASK, N)
                    fa.append(1)
                else:
                    fa.append(0)
                last_prices[feedcode]["ASK"] = cur_price_ASK

            cur_price_BID = tracker.FCHistories[feedcode]["BID"].price
            if cur_price_BID != last_prices[feedcode]["BID"]:
                last_ten_prices_BID = tracker.FCHistories[feedcode]["BID"].prices[-12:-2]
                good_price_BID = max(last_ten_prices_BID) - ((max(last_ten_prices_BID) - min(last_ten_prices_BID)) / m)
                if cur_price_BID > good_price_BID:
                    print("selling " + feedcode + str(last_ten_prices_BID) + ", " + str(cur_price_BID) + str(good_price_BID))
                    sender.send_order(feedcode, "SELL", cur_price_BID, N)
                    fb.append(1)
                else:
                    fb.append(0)
                last_prices[feedcode]["BID"] = cur_price_BID


