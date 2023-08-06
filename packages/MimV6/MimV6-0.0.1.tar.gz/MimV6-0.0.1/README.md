# mim_ipv6

## Description
Un package python pour performer un attaque de type "Man in the middle" avec Scapy, et de manipuler les paquets ip.

Le but de notre programme, consiste à usurper l'identité d'un destinataire dans une communication ipv6, pour voler des données au vrai           destinataire.

Les données une fois copiées seront tjr acheminée au vrai destinataire, pour que ce spoofing reste indetectable.

Notre programme n'est pas detectable en wifi, mais le deviens en ethernet.

## Requis
 - Python 3
 - Librairies standarts


## Installation

se mettre dans le dossier git et lancer :

```
pip install .

```

## Utilisation

```
mimV6

```
C'est un sniffeur de trame, qui une fois lancé, récupereras toutes les trames ipv6 du reseau sur lequel il est connecté. 

Le programme n'as besoin d'aucune interection utilisateur, et "spoofera", c'est à dire qu'il voleras, afficheras les trames volés sur votre terminal au format ASCII (droite) et hexadecimal(gauche), et enverras la trame volée aux différentes victime de son attaque.

le programme est codé pour tourner de façon constante et nécessite une interuption utilisateur (CTRL + C) pour être arrêté.

Nous avons aussi codé un outil de statistiques, qui fournira des info relatives à l'attaque que vous venez de lancer.

Les statistiques seronts affichés dès l'interruption utilisateur.


## Test
Nous avons crée des codes de test qui importent l'ensemble des fonctions nécessaire au fonctionnnement du code.

Ces test sont des fichiers indépendants qui peuvent êtres appellés à tout moment via :

```
pytest

```
## Exemples

Packetstat.py

```
from MimV6 import statistics, PacketStats
from scapy.all import Ether, IP, TCP, UDP, IPv6

statistics.append(PacketStats(Ether()))
statistics.append(PacketStats(Ether()/IP()))
statistics.append(PacketStats(Ether()/IP()/TCP()))
statistics.append(PacketStats(Ether()/IP()/UDP()))
statistics.append(PacketStats(Ether()/IPv6()/TCP()))
statistics.append(PacketStats(Ether()/IPv6()/UDP()))
statistics.append(PacketStats(Ether()/IPv6()))
statistics.append(PacketStats(Ether()))

print(f"""
UDP: {PacketStats.udp}
TCP: {PacketStats.tcp}
Other: {PacketStats.other}
""")

print("Lenght: " + ", ".join([str(pkt.lenght) for pkt in statistics]))

```

hexa_packet.py

```
from MimV6 import hexa_packet
from scapy.all import Ether, IP, TCP, UDP, IPv6
hexa_packet(Ether()/IP()/TCP())

hexa_packet(Ether())
hexa_packet(Ether()/IP())
hexa_packet(Ether()/IP()/TCP())
hexa_packet(Ether()/IP()/UDP())
hexa_packet(Ether()/IPv6()/TCP())
hexa_packet(Ether()/IPv6()/UDP())
hexa_packet(Ether()/IPv6())
hexa_packet(Ether())

```
mim_attack.py

```
from MimV6 import mim_attack
mim_attack()

```

## License
Licensed under the [GPL, version 3](https://www.gnu.org/licenses/).

## Lien
[Gitlab Page](https://gitlab.com/ChrisASSR/mim_ipv6_scapy)
