class Sender(object):
    def __init__(self, eml_sock, remote_ip, remote_port, username, password):
        self.eml_sock = eml_sock
        self.remote_ip = remote_ip
        self.remote_port = remote_port
        self.username = username
        self.password = password
        
    def send_order(self, target_feedcode, action, target_price, volume):
        """
        Send an order to the exchange.

        :param target_feedcode: The feedcode, either "SP-FUTURE" or "ESX-FUTURE"
        :param action: "BUY" or "SELL"
        :param target_price: Price you want to trade at
        :param volume: Volume you want to trade at. Please start with 10 and go from there. Don't go crazy!
        :return:

        Example:
        If you want to buy  100 SP-FUTURES at a price of 3000:
        - send_order("SP-FUTURE", "BUY", 3000, 100)
        """
        order_message = f"TYPE=ORDER|USERNAME={self.username}|PASSWORD={self.password}|FEEDCODE={target_feedcode}|ACTION={action}|PRICE={target_price}|VOLUME={volume}"
        print(f"[SENDING ORDER] {order_message}")
        self.eml_sock.sendto(order_message.encode(), (self.remote_ip, self.remote_port))
