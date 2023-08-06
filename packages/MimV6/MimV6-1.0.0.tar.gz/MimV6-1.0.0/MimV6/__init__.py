#!/usr/bin/env python3
# -*- coding: utf-8 -*-

""" This package implement a Man In the Middle attack in IPv6, a IPv6 Sniffer and a Statistic Packet Tool. """

###################
#    This package implement a Man In the Middle attack in IPv6, a IPv6 Sniffer and a Statistic Packet Tool.
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

__version__ = "1.0.0"
__all__ = [
    "mim_attack",
    "Sniffer",
    "PacketStats",
    "statistics",
    "Spoofer",
    "PacketPrinter",
]

from .Sniffer import Sniffer
from .Spoofer import Spoofer
from .PacketPrinter import PacketPrinter
from .MimV6 import main as mim_attack
from .PacketStats import PacketStats, stats as statistics

print(
    """
MimV6  Copyright (C) 2021  gitlab.com@ChrisASSR, gitlab.com@tHz_FireStorm, gitlab.com@lecorrem, gitlab.com@mrbouk
This program comes with ABSOLUTELY NO WARRANTY.
This is free software, and you are welcome to redistribute it
under certain conditions.
"""
)
