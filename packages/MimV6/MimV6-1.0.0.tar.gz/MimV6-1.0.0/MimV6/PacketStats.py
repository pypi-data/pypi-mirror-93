#!/usr/bin/env python3
# -*- coding: utf-8 -*-

""" This file implement PacketStats class for Statistic Packet Tool. """

###################
#    This file implement PacketStats class for Statistic Packet Tool.
#    Copyright (C) 2021  gitlab.com@ChrisASSR, gitlab.com@tHz_FireStorm, gitlab.com@lecorrem, gitlab.com@mrbouk

#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.

#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.

#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <https://www.gnu.org/licenses/>.
###################

from scapy.all import TCP, UDP

__all__ = ["PacketStats", "print_stats"]

global stats
stats = []


class PacketStats:

    """ This class implement the Statistic Packet Tool. """

    tcp = 0
    udp = 0
    other = 0

    def __init__(self, packet):
        if packet.haslayer(TCP):
            PacketStats.tcp += 1
        elif packet.haslayer(UDP):
            PacketStats.udp += 1
        else:
            PacketStats.other += 1
        self.lenght = len(packet)


def get_statistics(packet):
    global stats
    stats.append(PacketStats(packet))


def print_stats():
    print(
        f"""
Get {PacketStats.tcp + PacketStats.udp + PacketStats.other} IPv6 packets.
    - Get {PacketStats.tcp} TCP packets
    - Get {PacketStats.udp} UDP packets
    - Get {PacketStats.other} Other packets

Packet size average: { sum([packet_stat.lenght for packet_stat in stats]) / len(stats) if stats else 0 }
"""
    )
