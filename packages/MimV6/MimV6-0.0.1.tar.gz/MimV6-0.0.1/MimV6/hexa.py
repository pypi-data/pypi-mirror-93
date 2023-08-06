#!/usr/bin/env python3

import sys
from textwrap import wrap

def get_hexa (bytes_):
    hexa = "{:02X} " * len(bytes_)
    return hexa.format(*bytes_)

def get_printable (bytes_):
    printable = ""

    for car in bytes_:
        car = chr(car)
        if car in '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~ ':
            printable += car
        else:
            printable += "."

    return printable

def print_packet (packet):
    packet = bytes(packet)
    hexa = get_hexa(packet)

    printable = get_printable(packet)

    hexa = wrap(hexa, 48)
    printable = wrap(printable, 16)

    result = ""

    for i in range(len(hexa)):
        result += "{0:<53}".format(hexa[i]) + " " * 5 + printable[i] + "\n"

    print(result)
