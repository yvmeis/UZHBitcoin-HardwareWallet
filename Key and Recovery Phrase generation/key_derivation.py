import hashlib
import hmac
import phrasegenerator as pg



def master_key(seed):#seed as a bytestring
    h = hmac.new(b"Bitcoin seed", seed, digestmod = hashlib.sha512).digest()
    master_private_key = h[:32]
    chain_code = h[32:]
    print(master_private_key.hex())
    print(chain_code.hex())



seed = pg.gen_seed(pg.find_words(pg.hash_entropy(pg.gen_entropy(128), 128)))
master_key(seed)