#!/usr/bin/env python3
# -*- coding: utf-8 -*-

""" This file implement the main function to launch the mim attack with sniffer and statistic tools. """

###################
#    This file implement the main function to launch the mim attack with sniffer and statistic tools.
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

from argparse import ArgumentParser
from .Sniffer import Sniffer
from .Spoofer import Spoofer
from .PacketPrinter import PacketPrinter

__all__ = ["main"]


def parse():
    parser = ArgumentParser()
    parser.add_argument(
        "--no-hexa-sniffer",
        "-H",
        action="store_false",
        help="No print hexa sniffer",
        default=True,
    )
    parser.add_argument(
        "--summary-sniffer", "-s", action="store_true", help="Print summary sniffer"
    )
    parser.add_argument(
        "--details-sniffer", "-d", action="store_true", help="Print details sniffer"
    )
    parser.add_argument(
        "--details2-sniffer",
        "-D",
        action="store_true",
        help="Print details type 2 sniffer",
    )
    parser.add_argument(
        "--python-sniffer",
        "-p",
        action="store_true",
        help="Print python command sniffer",
    )
    parser.add_argument(
        "--raw-sniffer", "-r", action="store_true", help="Print raw sniffer"
    )
    parser.add_argument(
        "--info-sniffer", "-i", action="store_true", help="Print info sniffer"
    )

    parser.add_argument(
        "--target-sniffer",
        "-t",
        help='Print target packet only, use "all" to print all IPv6, use "None" to not sniff.',
        default="all",
    )
    parser.add_argument(
        "--save-filename-sniffer", "-S", help="Filename to save capture.", default=None
    )

    parser.add_argument("--target-spoofer", "-T", help="IPv6 to spoof", default="all")
    parser.add_argument(
        "--verbose-spoofer", "-v", action="store_true", help="Print summary spoofer"
    )

    return parser.parse_args()


def main():
    """ This function launch the mim attack with sniffer and statistic tools. """

    parser = parse()

    packet_printer = PacketPrinter(
        parser.no_hexa_sniffer,
        parser.summary_sniffer,
        parser.details_sniffer,
        parser.details2_sniffer,
        parser.python_sniffer,
        parser.raw_sniffer,
        parser.info_sniffer,
    )
    sniffer = Sniffer(parser.target_sniffer, packet_printer)
    spoofer = Spoofer(parser.target_spoofer, sniffer, parser.verbose_spoofer)

    sniffer.start()
    spoofer.launcher()


if __name__ == "__main__":
    main()
