import os, binascii, secrets, hashlib, sys

def generate_entropy():
    hexstring = binascii.b2a_hex(os.urandom(16))
    return hexstring
    

def generate_recovery_phrases(hexstring):
    phrases = bip39.mnemonic_from_bytes(hexstring)



################################################################

#length between 128 and 256. length has to be divisible by 32
def gen_entropy(length):
    entropy = os.urandom(length//8)
    return (entropy)

def hash_entropy(entropy, length):
    h = hashlib.sha256(entropy).hexdigest()
    b = bin(int(h, 16))[2:].zfill(256)
    checksum = b[0:int(length/32)]
    entropy_bytes = bin(int.from_bytes(entropy, byteorder = sys.byteorder))[2:].zfill(length)
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
    print(phrase)


find_words(hash_entropy(gen_entropy(128), 128))