"""

 PACKNET  -  c0mplh4cks

 PACKAGER


"""





# === Importing Dependencies === #
from . import ETHERNET
from . import ARP, IPv4, ICMP
from . import UDP, TCP
from . import DNS, MQTT
from . import RAW







# === Packager === #
class Packager():
    def __init__(self, packet=b""):
        self.packet = packet

        self.layer = []

        self.tree = {
            ETHERNET.Header : {
                0x0800 : IPv4.Header,
                0x0806 : ARP.Header
            },
            ARP.Header : {

            },
            IPv4.Header : {
                1 : ICMP.Header,
                6 : TCP.Header,
                17 : UDP.Header
            },
            ICMP.Header : {

            },
            TCP.Header : {
                1883 : MQTT.Header
            },
            UDP.Header : {
                53 : DNS.Header
            }
        }

        self.rtree = {
            DNS.Header : UDP.Header,
            MQTT.Header : TCP.Header,

            ICMP.Header : IPv4.Header,
            UDP.Header : IPv4.Header,
            TCP.Header : IPv4.Header,

            IPv4.Header : ETHERNET.Header,
            ARP.Header : ETHERNET.Header,

            ETHERNET.Header : None
        }



    def checkprotocol(self, protocol):
        if protocol.protocol == None: return RAW.Header

        l = protocol.protocol
        l = [l] if type(l) == int else l
        for p in list(l):
            if p in self.tree[ type(protocol) ]:
                return self.tree[ type(protocol) ][p]

        return RAW.Header



    def rcheckprotocol(self, first, second):
        d = { value : key for key, value in self.tree[first].items() }
        if second in d:
            return d[second]



    def read(self, next=ETHERNET.Header):
        packet = self.packet

        while True:
            current = next
            protocol = current(packet)
            protocol.read()

            self.layer.append( protocol )

            if type(protocol) == RAW.Header: break

            packet = protocol.data
            next = self.checkprotocol( protocol )

        return len(self.layer)



    def build(self, protocol):
        if type( protocol ) == RAW.Header: return None

        layer = []
        while True:
            layer.insert( 0, protocol() )
            protocol = self.rtree[protocol]
            if not protocol: break

        layer.append( RAW.Header() )

        for i in range( len(layer)-2 ):
            next = self.rcheckprotocol( type(layer[i]), type(layer[i+1]) )
            layer[i].protocol = next

        self.layer = layer

        return len(self.layer)
