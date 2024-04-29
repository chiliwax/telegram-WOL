"""
Determine a host's IP address given its MAC address and an IP address
range to scan for it.

I created this to discover a WLAN printer (which dynamically gets an IP
address assigned via DHCP) on the local network.

Calls Nmap_ to ping hosts and return their MAC addresses (requires root
privileges).

Requires Python_ 2.7+ or 3.3+.

.. _Nmap: http://nmap.org/
.. _Python: http://python.org/

:Copyright: 2014-2016 `Jochen Kupperschmidt
:Date: 27-Mar-2016 (original release: 25-Jan-2014)
:License: MIT
:Website: http://homework.nwsnet.de/releases/9577/#find-ip-address-for-mac-address
"""

import subprocess
import xml.etree.ElementTree as ET
def scan_for_hosts( ip_range):
    """Scan the given IP address range using Nmap and return the result
    in XML format.
    """
    nmap_args = ['nmap', '-n', '-sP', '-oX', '-', ip_range]
    return subprocess.check_output(nmap_args)


def find_ip_address_for_mac_address(xml, mac_address):
    """Parse Nmap's XML output, find the host element with the given
    MAC address, and return that host's IP address (or `None` if no
    match was found).
    """
    host_elems = ET.fromstring(xml).iter('host')
    host_elem = find_host_with_mac_address(host_elems, mac_address)
    if host_elem is not None:
        return find_ip_address(host_elem)


def find_host_with_mac_address(host_elems, mac_address):
    """Return the first host element that contains the MAC address."""
    for host_elem in host_elems:
        if host_has_mac_address(host_elem, mac_address):
            return host_elem


def host_has_mac_address(host_elem, wanted_mac_address):
    """Return true if the host has the given MAC address."""
    found_mac_address = find_mac_address(host_elem)
    return (
        found_mac_address is not None and
        found_mac_address.lower() == wanted_mac_address.lower()
    )


def find_mac_address(host_elem):
    """Return the host's MAC address."""
    return find_address_of_type(host_elem, 'mac')


def find_ip_address(host_elem):
    """Return the host's IP address."""
    return find_address_of_type(host_elem, 'ipv4')


def find_address_of_type(host_elem, type_):
    """Return the host's address of the given type, or `None` if there
    is no address element of that type.
    """
    address_elem = host_elem.find('./address[@addrtype="{}"]'.format(type_))
    if address_elem is not None:
        return address_elem.get('addr')