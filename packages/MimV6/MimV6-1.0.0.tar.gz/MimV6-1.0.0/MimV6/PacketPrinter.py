#!/usr/bin/env python3
# -*- coding: utf-8 -*-

""" This file implement PacketPrinter class. """

###################
#    This file implement PacketPrinter class.
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

from scapy.all import hexdump, raw, ls, packet

__all__ = ["PacketPrinter"]


class PacketPrinter:

    """ This class print packet with differents formats. """

    def __init__(
        self,
        hexa=True,
        summary=False,
        details1=False,
        details2=False,
        python=False,
        raw_=False,
        info=False,
    ):
        self.functions = []

        if hexa:
            self.functions.append(hexdump)
        if summary:
            self.functions.append(self.print_summary)
        if details1:
            self.functions.append(packet.Packet.show)
        if details2:
            self.functions.append(packet.Packet.show2)
        if python:
            self.functions.append(self.print_command)
        if raw_:
            self.functions.append(self.print_raw)
        if info:
            self.functions.append(ls)

    def print_command(self, packet):
        print(packet.command())

    def print_summary(self, packet):
        print(packet.summary())

    def print_raw(self, packet):
        print(raw(packet))

    def print(self, packet):
        for function in self.functions:
            function(packet)
