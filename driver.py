from netifaces import interfaces, ifaddresses, AF_INET
from typing import Optional

import server
import globals

def start_server() -> Optional[int]:
    for port in globals.port_options:
        return port
    return None


def connect_to_mobile(port: int):
    globals.connection_secret = input("Enter Connection Secret: ")
    ip_list = []
    for interface in interfaces():
        try:
            for link in ifaddresses(interface)[AF_INET]:
                ip_list.append(f"http://{link['addr']}:{port}")
        except KeyError:
            pass
    print("Try connecting to any 1 of these:")
    print(" or ".join(ip_list))

def main():
    port = start_server()
    if not port:
        print("Cannot start the driver")
        exit(1)
    connect_to_mobile(port)
    server.serve(port)


if __name__ == '__main__':
    main()
