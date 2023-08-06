from .PacketPrinter import PacketPrinter
from scapy.all import Ether, IPv6, UDP


def test_PacketPrinter_print():
    PacketPrinter(True, True, True, True, True, True, True).print(
        Ether() / IPv6() / UDP()
    )
