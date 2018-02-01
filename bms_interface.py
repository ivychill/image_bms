import socket

class BmsInterface:
    def __init__(self):
        # try:
        self.image_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # self.adress = ("192.168.24.92", 13000)
        # self.adress = ("192.168.20.114", 13000)
        self.adress = ("192.168.20.122", 13000)
        self.image_socket.connect(self.adress)
        # except Exception, e:
        #     return 0
        self.command_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        # self.command_addr = ("192.168.24.92", 4001)
        self.command_addr = ("192.168.20.122", 4001)
        # self.command_addr = ("192.168.20.114", 13000)

    # def move_td(self, msg):
    #     self.command_socket.sendto("K:101", self.command_addr)