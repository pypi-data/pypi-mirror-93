"""

 PACKNET  -  c0mplh4cks

 INTERFACE


"""





# === Importing Dependencies === #
import socket
from time import time
from .standards import encode, decode
from .packager import Packager
from . import ETHERNET
from . import ARP







# === Interface === #
class Interface():
    def __init__(self, card=None, port=0, passive=False):
        self.passive = passive
        self.timeout = 1

        self.sock = socket.socket( socket.AF_PACKET, socket.SOCK_RAW, socket.htons(0x0003) )


        if not card:
            self.card = [ i[1] for i in socket.if_nameindex() ][-1]
        else:
            self.card = card

        if not passive:
            s = socket.socket( socket.AF_INET, socket.SOCK_DGRAM )
            s.setsockopt( socket.SOL_SOCKET, 25, f"{ self.card }".encode() )
            s.connect( ("1.1.1.1", 80) )
            ip = s.getsockname()[0]

            self.sock.bind( (self.card, 0) )
            mac = decode.mac( self.sock.getsockname()[4] )

            self.addr = ( ip, port, mac )



    def send(self, packet):
        self.sock.send(packet)

    def recv(self, length=2048):
        return self.sock.recvfrom(length)



    def getmac(self, ip):
        if self.passive: return None

        arp = ARP.Header()
        arp.op = 1
        arp.src = self.addr
        arp.dst = [ip, 0, "00:00:00:00:00:00"]
        arp.build()

        ethernet = ETHERNET.Header()
        ethernet.protocol = 0x0806
        ethernet.src = self.addr
        ethernet.dst = ["", 0, "ff:ff:ff:ff:ff:ff"]
        ethernet.data = arp.packet
        ethernet.build()

        self.send( ethernet.packet )

        start = time()
        while ( time()-start < self.timeout ):
            packet, info = self.recv()

            package = Packager(packet)
            package.read()

            if len( package.layer ) < 2: continue
            if type( package.layer[1] ) != ARP.Header: continue
            if package.layer[1].dst[2] != self.addr[2]: continue
            if package.layer[1].src[0] != ip: continue

            return package.layer[1].src
