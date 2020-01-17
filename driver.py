from netifaces import interfaces, ifaddresses, AF_INET
from typing import Optional

import server
import globals
import firewall


def start_server() -> Optional[int]:
    for port in globals.port_options:
        if firewall.open_port(port):
            return port
    return None


def connect_to_mobile(port: int):
    globals.connection_secret = input("Enter Connection Secret: ")
    # from socket import getaddrinfo, AF_INET, gethostname
    # ip_list = [ip[4][0] for ip in getaddrinfo(host=gethostname(), port=None, family=AF_INET)]
    ip_list = []
    for interface in interfaces():
        try:
            for link in ifaddresses(interface)[AF_INET]:
                ip_list.append(f"{link['addr']}:{port}")
        except KeyError:
            pass
    print("Try connecting to any 1 of these:")
    print(" or ".join(ip_list))


def handle_controls():
    pass


def main():
    port = start_server()
    if not port:
        print("Cannot start the driver")
        exit(1)
    connect_to_mobile(port)
    server.serve(port)


if __name__ == '__main__':
    main()
