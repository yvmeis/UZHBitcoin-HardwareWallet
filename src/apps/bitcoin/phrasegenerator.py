import os
import unicodedata
from typing import AnyStr
from . import hash_collection as ha

# length between 128 and 256. length has to be divisible by 32

def gen_entropy(length: int) -> bytes:
    '''generates a random bytestring of given length'''
    
    entropy = os.urandom(length//8)
    return entropy


def hash_entropy(entropy: bytes, length: int) -> bin:
    '''hashes the given entropy'''
    
    h = ha.sha256(entropy).hexdigest()

    b = bin(int(h, 16))[2:].zfill(256)
    checksum = b[0:int(length/32)]
    entropy_bytes = bin(int.from_bytes(entropy, byteorder='big'))[
        2:].zfill(length)
    mnemonic_bytes = entropy_bytes + checksum
    return mnemonic_bytes


def find_words(binary: bin) -> list:
    '''extracts mnemonic words from the word list'''
    
    path = 'src/apps/bitcoin/english.txt'
    if not os.path.exists('src/apps/bitcoin/english.txt'):
        path = 'english.txt'
    file = open(path, 'r')
    words = []
    phrase = []
    for x in file:
        words.append(x)
    file.close()
    for x in range(0, len(binary), 11):
        phrase.append(words[int(binary[x:x+11], 2)].rstrip())
        # print(int(binary[x:x+11],2))
    # print(phrase)
    return phrase


def gen_seed(words: list, passphrase='') -> bytes:
    '''generates a seed from the mnemonic words and an optional passphrase'''
    
    sentence = " ".join(words)
    password = normalize_string(sentence)
    passphrase = normalize_string(passphrase)
    salt = 'mnemonic' + passphrase
    salt = salt.encode('utf-8')
    password = password.encode('utf-8')
    seed = ha.seed_hash(password, salt)
    return seed[:64]


def normalize_string(txt: AnyStr) -> str:
    '''normalizes given string'''
    
    if isinstance(txt, bytes):
        utxt = txt.decode("utf8")
    elif isinstance(txt, str):
        utxt = txt
    else:
        raise TypeError("String value expected")

    return unicodedata.normalize("NFKD", utxt)

