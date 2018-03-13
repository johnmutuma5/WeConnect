import random

def generate_token ():
    chars = ""
    for i in range(26):
        chars += chr (65+i)
        chars += chr (97+i)

    token = ""
    for i in range(96):
        rand_index = random.randint(0, 51)
        token += chars[rand_index]
    return token
