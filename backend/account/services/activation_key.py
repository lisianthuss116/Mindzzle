import hashlib
import random


def activation_code(key):
    salt = hashlib.sha256(str(random.random()).encode(
        'utf-8')).hexdigest()[:16]

    str_hash = str(key) + str(salt)
    return hashlib.sha256(str_hash.encode('utf-8')).hexdigest()[18:50]

print(activation_code('ahdnf27rgn82'))