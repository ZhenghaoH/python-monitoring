#!/usr/bin/env python3
import os
import sys


from scapy.all import IPv6, TCP, get_if_list, sniff, UDP
from int_header import *
HOPS = 3
ShimSize = 4
INTSize = 12
MetadataSize = 26


def get_if():
    ifs=get_if_list()
    iface=None
    for i in get_if_list():
        if "eth0" in i:
            iface=i
            break;
    if not iface:
        print("Cannot find eth0 interface")
        exit(1)
    return iface

def handle_pkt(pkt):
    if int_shim_header in pkt :
        print("got a packet")
        # pkt.show()
#        hexdump(pkt)
#        print "len(pkt) = ", len(pkt)
        p1 = pkt.copy()

        p1 = p1.payload.payload.payload

        p1_bytes = bytes(p1)

        int_shim_header(p1_bytes[0:ShimSize]).show()
        p1_bytes = p1_bytes[ShimSize:]

        int_header(p1_bytes[0:INTSize]).show()
        p1_bytes = p1_bytes[INTSize:]

        for i in range(HOPS):
            p2 = int_metadata(p1_bytes[0:MetadataSize])
            p2.show()
            p1_bytes = p1_bytes[MetadataSize:]
        sys.stdout.flush()


def main():
    ifaces = [i for i in os.listdir('/sys/class/net/') if 'eth' in i]
    iface = get_if()
    print("sniffing on %s" % iface)
    sys.stdout.flush()
    sniff(iface = iface,
          prn = lambda x: handle_pkt(x))

if __name__ == '__main__':
    main()
