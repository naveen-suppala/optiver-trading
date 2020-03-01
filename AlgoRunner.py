import threading
import datetime

class Algo1(threading.Thread):
    FEEDCODES = ["SP-FUTURE", "ESX-FUTURE"]

    def __init__(self, tracker, sender, N=80):
        self.tracker = tracker
        self.sender = sender
        self.N = N
        self.m1 = {"ESX-FUTURE": 4, "SP-FUTURE": 4}
        self.m2 = {"ESX-FUTURE": 5, "SP-FUTURE": 5}
        self.bought = {"ESX-FUTURE": [], "SP-FUTURE": []}
        self.last_prices = {
                "ESX-FUTURE": {
                    "ASK": None,
                    "BID": None
                    },
                "SP-FUTURE": {
                    "ASK": None,
                    "BID": None
                    }
                }
        super().__init__()

    def algo1(self):
        for feedcode in self.FEEDCODES:
            cur_price_ASK = self.tracker.FCHistories[feedcode]["ASK"].price
            if cur_price_ASK != self.last_prices[feedcode]["ASK"]:
                last_ten_prices_ASK = self.tracker.FCHistories[feedcode]["ASK"].prices[-12:-2]
                good_price_ASK = min(last_ten_prices_ASK) + ((max(last_ten_prices_ASK) - min(last_ten_prices_ASK)) / self.m1[feedcode])
                if cur_price_ASK < good_price_ASK:
                    print("buying " + feedcode + str(last_ten_prices_ASK) + ", " + str(cur_price_ASK) + ", " + str(good_price_ASK))
                    self.sender.send_order(feedcode, "BUY", cur_price_ASK, self.N)
                    self.bought[feedcode].append(datetime.datetime.now())
                self.last_prices[feedcode]["ASK"] = cur_price_ASK

            cur_price_BID = self.tracker.FCHistories[feedcode]["BID"].price
            if cur_price_BID != self.last_prices[feedcode]["BID"]:
                last_ten_prices_BID = self.tracker.FCHistories[feedcode]["BID"].prices[-12:-2]
                good_price_BID = max(last_ten_prices_BID) - ((max(last_ten_prices_BID) - min(last_ten_prices_BID)) / self.m2[feedcode])
                if cur_price_BID > good_price_BID:
                    print("selling " + feedcode + str(last_ten_prices_BID) + ", " + str(cur_price_BID) + str(good_price_BID))
                    self.sender.send_order(feedcode, "SELL", cur_price_BID, self.N)
                    self.bought[feedcode].append(datetime.datetime.now())
                self.last_prices[feedcode]["BID"] = cur_price_BID

    def run(self):
        while True:
            self.algo1()
