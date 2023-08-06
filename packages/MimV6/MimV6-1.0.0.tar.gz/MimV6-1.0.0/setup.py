#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

setup(
    name="MimV6",
    version="1.0.0",
    packages=find_packages(include=["MimV6"]),
    install_requires=["scapy"],
    author="gitlab.com@ChrisASSR, gitlab.com@tHz_FireStorm, gitlab.com@lecorrem, gitlab.com@mrbouk",
    author_email="mauricelambert434@gmail.com",
    description="This package implement a Man In the Middle attack in IPv6, a IPv6 Sniffer and a Statistic Packet Tool.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    include_package_data=True,
    url="https://gitlab.com/ChrisASSR/mim_ipv6_scapy",
    classifiers=[
        "Programming Language :: Python",
        "Development Status :: 5 - Production/Stable",
        "Environment :: Console",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.8",
    ],
    entry_points={
        "console_scripts": ["mimV6 = MimV6:mim_attack"],
    },
    python_requires=">=3.6",
)
