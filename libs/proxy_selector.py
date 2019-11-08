import random

proxy_list = [
    "37.48.118.90:13042",
    "83.149.70.159:13042"
]


def get_random_proxy():
    return random.choice(proxy_list)