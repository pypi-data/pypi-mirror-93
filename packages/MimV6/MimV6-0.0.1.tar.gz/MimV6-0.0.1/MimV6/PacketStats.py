from scapy.all import TCP, UDP

global stats
stats = []

class PacketStats:

    tcp = 0
    udp = 0
    other = 0

    def __init__ (self, packet):
        if packet.haslayer(TCP):
            PacketStats.tcp += 1
        elif packet.haslayer(UDP):
            PacketStats.udp += 1
        else:
            PacketStats.other += 1
        self.lenght = len(packet)

def get_statistics (packet):
    global stats
    stats.append(PacketStats(packet))

def print_stats ():
    print(f"""
Get {PacketStats.tcp + PacketStats.udp + PacketStats.other} IPv6 packets.
    - Get {PacketStats.tcp} TCP packets
    - Get {PacketStats.udp} UDP packets
    - Get {PacketStats.other} Other packets

Packet size average: { sum([packet_stat.lenght for packet_stat in stats]) / len(stats) if stats else 0 }
""")
