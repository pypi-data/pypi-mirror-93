from setuptools import setup, find_packages

setup(
    name = 'MimV6',
 
    version = "0.0.1",
    packages = find_packages(include=["MimV6"]),
    install_requires = ['scapy'],
 
    description = "This package implement command line and python package tool for Man In The Middle in IPv6.",
    long_description = open('README.md').read(),
    long_description_content_type="text/markdown",
 
    include_package_data = True,

    url = 'https://gitlab.com/ChrisASSR/mim_ipv6_scapy',
 
    classifiers = [
        "Programming Language :: Python",
        "Development Status :: 5 - Production/Stable",
        "Environment :: Console",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.8"
    ],
 
    entry_points = {
        'console_scripts': [
            'mimV6 = MimV6:mim_attack'
        ],
    },
    python_requires='>=3.6',
)