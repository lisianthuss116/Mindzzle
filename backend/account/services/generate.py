import hashlib
import random


def set_user_id(number):
    salt = hashlib.sha256(str(random.random()).encode('utf-8')).hexdigest()[:8]
    set_id = str(number * 264782)

    user_id = str(salt[0:4]) + set_id
    return user_id


def get_real_user_id(number):
    get_id = number[4:None]
    set_id = int(get_id) / 264782

    user_id = int(set_id)
    return user_id
