import hashlib
import hmac
import phrasegenerator as pg
import base58
import btclib as bit
import bitcoin
import codecs
import unicodedata


def generate_master_private_key(seed):#seed as a bytestring
    key = "Bitcoin seed"
    key = key.encode(encoding = 'UTF-8')
    h = hmac.new(key, seed, digestmod = hashlib.sha512).digest()
    master_private_key = h[:32]
    chain_code = h[32:]
    extended_master_private_key = (master_private_key, chain_code)
    return extended_master_private_key

def serialize(extended_key: tuple, prv_pbl: str, derivation_level: str, net = 'mainnet', fingerprint = '00000000', childnumber = '00000000'): 
    '''remove '0x' from all hex strings'''
    #extended_key: tuple with [0] = TYPE BYTE: key, [1] = TYPE BYTE: chain code
    #prv_bl = TYPE STRING: 'private'/'public'; 
    #derivation_level = TYPE HEXSTRING: 0x00 for master, 0x01 for level-1 derived, ...
    #net = TYPE STRING: 'mainnet'/'testnet'
    #fingerprint = TYPE HEXSTRING: 0x00000000 for master, fingerprint of the parent's key for children
    #childnumber = TYPE HEXSTRING: 0x00000000 for master, ??? for children
    
    
    specs = {'mainnet': {'public': '0488B21E', 'private': '0488ADE4'}, 'testnet': {'public': '043587CF', 'private': '04358394'},
             }
    
    serialized_key = bytes.fromhex(specs[net][prv_pbl])
    serialized_key += bytes.fromhex(derivation_level)
    serialized_key += bytes.fromhex(fingerprint)
    
    if derivation_level == '00':
        serialized_key += bytes.fromhex(childnumber) #for master
    if derivation_level != '00':
        pass #children: still to be done
    serialized_key += extended_key[1]
    
    if prv_pbl == 'private':
        serialized_key += bytes.fromhex('00') + extended_key[0]
    if prv_pbl == 'public':
        pass #public key: still to be done
        
    hashed_serialized_key = hashlib.sha256(serialized_key).digest()
    hashed_serialized_key = hashlib.sha256(hashed_serialized_key).digest()

    serialized_key += hashed_serialized_key[:4]
    return encode_b58(serialized_key)
    
    
def encode_b58(ser_key):
    encoded_key = base58.b58encode(ser_key)
    return encoded_key

def derive_child(prv_key, i): 
    #   2**31 <= i <= 2**32-1 ---> hardened key derivation
    #   0 <= i <= 2**31-1 ---> non-hardened derivation
    der = bitcoin.bip32_ckd(prv_key, i)
    return der

def prv_to_pub(prv_key):
    pub = bitcoin.bip32_privtopub(prv_key)
    return pub
    
def gen_address(pub_key):
    pub_key = bytes.fromhex(pub_key)
    hashed256 = hashlib.new('sha256', pub_key).digest()
    hashed160 = hashlib.new('ripemd160', hashed256).digest()
    hashed160v = bytes.fromhex('00') + hashed160 # 00 for mainnet bitcoin
    b58_hashed256_1 = hashlib.new('sha256', hashed160v).digest()
    b58_hashed256_2 = hashlib.new('sha256', b58_hashed256_1).digest()
    address_checksum = b58_hashed256_2[:4]
    bin_btc_address = hashed160v + address_checksum
    address = encode_b58(bin_btc_address)
    return address
    

seed = pg.gen_seed(pg.find_words(pg.hash_entropy(pg.gen_entropy(128), 128)))
master = serialize(generate_master_private_key(seed), prv_pbl = 'private', derivation_level = '00')
print(master)
der = derive_child(master, 0)
print(der)
pub = prv_to_pub(der)
print(pub)
address = gen_address(pub)
print(address)
