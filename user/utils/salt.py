import random


def get_salt():
    l1 = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v',
          'w', 'x', 'y', 'z']
    l2 = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0']
    l3 = [',', '!', '@', '#', '$', '%', '^', '&', '*', '<', '>', '.']
    l = l1 + l2 + l3

    salt = "".join(random.sample(l, 8)).replace(" ", "")
    return salt