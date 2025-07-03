import random

PROXIES = [
    "socks5://user1:pass1@proxy1:1080",
    "socks5://user2:pass2@proxy2:1080",
]

def get_random_proxy():
    return random.choice(PROXIES)
