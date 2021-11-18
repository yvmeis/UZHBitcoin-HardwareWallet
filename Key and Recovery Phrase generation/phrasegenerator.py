import os, binascii, secrets, hashlib, sys, unicodedata

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

def gen_seed(mnemonic_bytes, passphrase = 'TREZOR'):
    # The passphrase is a phrase the user should be able to choose in order to make things more secure!
    password = mnemonic_bytes.hex()
    password = unicodedata.normalize('NFKD', password)
    salt = 'mnemonic' + passphrase
    salt = unicodedata.normalize('NFKD', salt)
    iterations = 2048
    salt = salt.encode('utf-8')
    password = password.encode('utf-8')
    seed = hashlib.pbkdf2_hmac('sha512',password,salt,iterations)
    return seed
     
find_words(hash_entropy(gen_entropy(128), 128))


################################################################################################
#########################################tests##################################################
################################################################################################

ma_seed = gen_seed(bytes.fromhex('c55257c360c07c72029aebc1b53c05ed0362ada38ead3e3e9efa3708e53495531f09a6987599d18264c1e1c92f2cf141630c7a3c4ab7c81b2f001698e7463b04'))
print (ma_seed.hex())