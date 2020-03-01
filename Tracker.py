import select
import threading
import datetime


class Tracker(threading.Thread):
    IML_INIT_MESSAGE = "TYPE=SUBSCRIPTION_REQUEST"

    def __init__(self, iml_sock, remote_ip, remote_port, callback=None):
        self.iml_sock = iml_sock
        self.remote_ip = remote_ip
        self.remote_port = remote_port
        self.callback = callback
        self.FCHistories = {
                "ESX-FUTURE": {
                    "ASK": PriceHistory(),
                    "BID": PriceHistory()
                    },
                "SP-FUTURE": {
                    "ASK": PriceHistory(),
                    "BID": PriceHistory()
                    },
                "Timestamp": []
                }
        self.should_run = None
        super().__init__()

    def subscribe(self):
        self.iml_sock.sendto(self.IML_INIT_MESSAGE.encode(), (self.remote_ip, self.remote_port))

    def run(self):
        self.should_run = True
        self.subscribe()
        while self.should_run:
            ready_socks, _, _ = select.select([self.iml_sock], [], [])
            if ready_socks:
                data, _ = self.iml_sock.recvfrom(1024)
                x = list(map(lambda x: x.split("=")[1], data.decode("utf-8").split("|")))
                if (len(x) != 6):
                    # print("AAAAAAAh: " + data.decode("utf-8"))
                    pass
                else:
                    [TYPE, FEEDCODE, BID_PRICE, BID_VOLUME, ASK_PRICE, ASK_VOLUME] = x
                    if TYPE == "PRICE":
                        self.FCHistories[FEEDCODE]["BID"].prices.append(float(BID_PRICE))
                        self.FCHistories[FEEDCODE]["BID"].price = float(BID_PRICE)
                        self.FCHistories[FEEDCODE]["BID"].volumes.append(float(BID_VOLUME))
                        self.FCHistories[FEEDCODE]["BID"].volume = float(BID_VOLUME)
                        self.FCHistories[FEEDCODE]["ASK"].prices.append(float(ASK_PRICE))
                        self.FCHistories[FEEDCODE]["ASK"].price = float(ASK_PRICE)
                        self.FCHistories[FEEDCODE]["ASK"].volumes.append(float(ASK_VOLUME))
                        self.FCHistories[FEEDCODE]["ASK"].volume = float(ASK_VOLUME)
                        self.FCHistories["Timestamp"].append(datetime.datetime.now())
                    if self.callback:
                        self.callback(TYPE, FEEDCODE, BID_PRICE, BID_VOLUME, ASK_PRICE, ASK_VOLUME)

    def stop_running(self):
        self.should_run = False
        self.join()

class PriceHistory(object):
    def __init__(self):
        self.prices = []
        self.price = None
        self.volumes = []
        self.volume = None
