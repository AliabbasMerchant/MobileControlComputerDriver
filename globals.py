import random

connection_secret = None
port_options = [3124, random.randint(1025, 65536), random.randint(1025, 65536)]
port_was_opened = False
