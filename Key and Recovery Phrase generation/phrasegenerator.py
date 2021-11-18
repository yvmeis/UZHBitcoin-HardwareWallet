import os, binascii, secrets, hashlib


#length between 128 and 256. length has to be divisible by 32
def gen_entropy(length):
    entropy = os.urandom(length//8)
    print(entropy)
    return (entropy)

def hash_entropy(entropy):
    h = hashlib.sha256(entropy).hexdigest()
    print()
    print(h)
    b = (
            bin(int.from_bytes(entropy, byteorder="big"))[2:].zfill(len(entropy) * 8)
            + bin(int(h, 16))[2:].zfill(256)[: len(entropy) * 8 // 32]
        )
    print()
    print(str(b))
    return str(b)
    
    
    
    
    #x = hashlib.sha256()
    #x.update(entropy)
    #hashed_entropy = x.digest()
    
    #return hashed_entropy
    
def find_words(binary):
    file = open('english.txt', 'r')
    words = []
    phrase = ""
    for x in file:
        words.append(x)
    file.close()
    for x in range(0, len(binary), 11):
        print(int(binary[x:x+11], 2))
        phrase = phrase + words[int(binary[x:x+11], 2)] + " "
    print(phrase)

a = hash_entropy(gen_entropy(128))
find_words(a)