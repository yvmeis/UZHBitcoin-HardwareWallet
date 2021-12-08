import hashlib, hmac

'''
A collection of the hashes used in the entire program
'''

def seed_hash(password: bytes, salt: bytes):
    iterations = 2048
    seed = hashlib.pbkdf2_hmac('sha512', password, salt, iterations)
    return seed

def sha256(hashable):
    hashed = hashlib.sha256(hashable)
    return hashed

def ripemd160(hashable):
    hashed = hashlib.new('ripemd160', hashable)
    return hashed

def hmacsha256(hashable1, hashable2):
    hashed = hmac.new(hashable1, hashable2, digestmod = hashlib.sha512)
    return hashed