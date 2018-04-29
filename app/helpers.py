import random
from .exceptions import MissingDataError

def generate_token ():
    chars = ""
    for i in range(26):
        chars += chr (65+i)
        chars += chr (97+i)
        if i > 9:
            continue
        chars += str(i)

    token = ""
    for i in range(96):
        rand_index = random.randint(0, 61)
        token += chars[rand_index]
    return token


def inspect_data(data, required_fields=None):
    '''
        Removes extra spaces in data and checks for blank fields
    '''
    if not required_fields:
        required_fields = data.keys()

    for field in required_fields:
        field_value = str(data.get(field, "")).strip()
        if not len(field_value):
            raise MissingDataError(msg='Please provide %s' %field)
        field_value = " ".join(field_value.split())
        data[field] = field_value

    return data
