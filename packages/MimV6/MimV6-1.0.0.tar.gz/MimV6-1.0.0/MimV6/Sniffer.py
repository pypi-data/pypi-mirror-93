#!/usr/bin/env python3
# -*- coding: utf-8 -*-

""" This file implement Sniffer class. """

###################
#    This file implement Sniffer class.
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

from scapy.all import AsyncSniffer, IPv6
from .PacketStats import get_statistics, print_stats

__all__ = ["Sniffer"]


class Sniffer:
    def __init__(self, target="all", packet_printer=None, savefile=None):
        self.target = target
        self.packet_printer = packet_printer
        self.packets = []
        self.savefile = savefile

        if target == "all":
            self.filter = lambda packet: packet.haslayer(IPv6)
        elif target == "None":
            self.filter = lambda packet: False
        else:
            self.filter = lambda packet: packet.haslayer(IPv6) and (
                packet.getlayer(IPv6).src == self.target
                or packet.getlayer(IPv6).dst == self.target
            )

        self.sniffer = AsyncSniffer(
            lfilter=self.filter, prn=lambda packet: self.analysis(packet)
        )

    def start(self):
        if self.target != "None":
            self.sniffer.start()

    def stop(self):
        if self.target != "None":
            self.sniffer.start()
        if self.savefile:
            wrpcap(self.savefile, self.packets)
        print_stats()

    def analysis(self, packet):
        if self.packet_printer:
            self.packet_printer.print(packet)
        if self.savefile:
            self.packets.append(packet)
        get_statistics(packet)
