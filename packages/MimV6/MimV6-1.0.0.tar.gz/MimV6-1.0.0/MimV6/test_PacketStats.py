from scapy.all import Ether, IPv6, TCP, UDP, ICMPv6EchoRequest
from .PacketStats import get_statistics, PacketStats, stats, print_stats


def test_get_statistics():
    get_statistics(Ether() / IPv6() / TCP())
    get_statistics(Ether() / IPv6() / UDP())
    get_statistics(Ether() / IPv6())
    get_statistics(Ether() / IPv6() / ICMPv6EchoRequest())

    assert len(stats) == 4
    assert PacketStats.tcp == 1
    assert PacketStats.udp == 1
    assert PacketStats.other == 2

    for packet_stat in stats:
        assert packet_stat.lenght >= len(Ether() / IPv6())


def test_PacketStats_constructor():
    packet_stat = PacketStats(Ether() / IPv6() / TCP())

    assert packet_stat.lenght == len(Ether() / IPv6() / TCP())
    assert packet_stat.tcp == 2
    assert PacketStats.tcp == 2

    assert packet_stat.udp == 1
    assert PacketStats.udp == 1

    assert packet_stat.other == 2
    assert PacketStats.other == 2
