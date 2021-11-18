import os, binascii, secrets, hashlib, sys, unicodedata
from typing import AnyStr

#length between 128 and 256. length has to be divisible by 32
def gen_entropy(length):
    entropy = os.urandom(length//8)
    print(entropy)
    print()
    return entropy

def hash_entropy(entropy, length):
    h = hashlib.sha256(entropy).hexdigest()
    print("hash")
    print(h)
    print()
    
    b = bin(int(h, 16))[2:].zfill(256)
    checksum = b[0:int(length/32)]
    print(checksum)
    entropy_bytes = bin(int.from_bytes(entropy, byteorder = 'big'))[2:].zfill(length)
    print(entropy_bytes)
    mnemonic_bytes = entropy_bytes + checksum
    return mnemonic_bytes
    
def find_words(binary):
    file = open('english.txt', 'r')
    words = []
    phrase = []
    for x in file:
        words.append(x)
    file.close()
    for x in range(0, len(binary), 11):
        phrase.append(words[int(binary[x:x+11], 2)].rstrip())
        print(int(binary[x:x+11],2))
    print(phrase)
    return phrase

def gen_seed(words, passphrase = ''):
    sentence = " ".join(words)
    print(sentence)    
    password = normalize_string(sentence)
    passphrase = normalize_string(passphrase)
    salt = 'mnemonic' + passphrase
    iterations = 2048
    salt = salt.encode('utf-8')
    password = password.encode('utf-8')
    seed = hashlib.pbkdf2_hmac('sha512', password, salt, iterations)
    return seed[:64]

def normalize_string(txt: AnyStr) -> str:
        if isinstance(txt, bytes):
            utxt = txt.decode("utf8")
        elif isinstance(txt, str):
            utxt = txt
        else:
            raise TypeError("String value expected")

        return unicodedata.normalize("NFKD", utxt)
     
find_words(hash_entropy(gen_entropy(128), 128))


################################################################################################
#########################################tests##################################################
################################################################################################

ma_seed = gen_seed(find_words(hash_entropy(gen_entropy(128), 128)))
print()
print (ma_seed.hex())