import os
import unicodedata
from typing import AnyStr
import src.apps.bitcoin.hash_collection as ha

# length between 128 and 256. length has to be divisible by 32


def gen_entropy(length):
    entropy = os.urandom(length//8)
    return entropy


def hash_entropy(entropy, length):
    h = ha.sha256(entropy).hexdigest()

    b = bin(int(h, 16))[2:].zfill(256)
    checksum = b[0:int(length/32)]
    entropy_bytes = bin(int.from_bytes(entropy, byteorder='big'))[
        2:].zfill(length)
    mnemonic_bytes = entropy_bytes + checksum
    return mnemonic_bytes


def find_words(binary):
    file = open('src/apps/bitcoin/english.txt', 'r')
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


def gen_seed(words, passphrase=''):
    sentence = " ".join(words)
    password = normalize_string(sentence)
    passphrase = normalize_string(passphrase)
    salt = 'mnemonic' + passphrase
    salt = salt.encode('utf-8')
    password = password.encode('utf-8')
    seed = ha.seed_hash(password, salt)
    return seed[:64]


def normalize_string(txt: AnyStr) -> str:
    if isinstance(txt, bytes):
        utxt = txt.decode("utf8")
    elif isinstance(txt, str):
        utxt = txt
    else:
        raise TypeError("String value expected")

    return unicodedata.normalize("NFKD", utxt)


def main():
    find_words(hash_entropy(gen_entropy(128), 128))
    ma_seed = gen_seed(find_words(hash_entropy(gen_entropy(128), 128)))


if __name__ == "__main__":
    # stuff only to run when not called via 'import' here
    main()
