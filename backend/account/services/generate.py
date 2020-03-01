import hashlib
import random


def set_user_id(number):
    # generate uniq-str
    salt = hashlib.sha256(str(random.random()).encode('utf-8')).hexdigest()[:8]
    # create fake-user-id
    set_id = str(number * 26845)

    # set uniq-str 4-char in front and set the user-id in the-rest
    user_id = str(salt[0:6]) + set_id
    return user_id


def get_real_user_id(number):
    # get user-id after 4-character-in-the-front
    get_id = number[6:None]
    # get real-user-id
    set_id = int(get_id) / 26845

    user_id = int(set_id)
    return user_id
