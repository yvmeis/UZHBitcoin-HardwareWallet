import hashlib
import hmac
import phrasegenerator as pg



def generate_master_private_key(seed):#seed as a bytestring
    key = "Bitcoin seed"
    key = key.encode(encoding = 'UTF-8')
    h = hmac.new(key, seed, digestmod = hashlib.sha512).digest()
    master_private_key = h[:32]
    chain_code = h[32:]
    print(master_private_key)
    print(chain_code)
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
        serialized_key += bytes.fromhex('00') # + ??? for private key: still to be done
    if prv_pbl == 'public':
        pass #public key: still to be done

############YOINKED CODE#########################
def b58encode(v: bytes) -> str:
    alphabet = "123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz"

    p, acc = 1, 0
    for c in reversed(v):
        acc += p * c
        p = p << 8

    string = ""
    while acc:
        acc, idx = divmod(acc, 58)
        string = alphabet[idx : idx + 1] + string
    return string

def to_hd_master_key(seed: bytes, testnet: bool = False) -> str:
        if len(seed) != 64:
            raise ValueError("Provided seed should have length of 64")

        # Compute HMAC-SHA512 of seed
        seed = hmac.new(b"Bitcoin seed", seed, digestmod=hashlib.sha512).digest()

        # Serialization format can be found at: https://github.com/bitcoin/bips/blob/master/bip-0032.mediawiki#Serialization_format
        xprv = b"\x04\x88\xad\xe4"  # Version for private mainnet
        if testnet:
            xprv = b"\x04\x35\x83\x94"  # Version for private testnet
        xprv += b"\x00" * 9  # Depth, parent fingerprint, and child number
        xprv += seed[32:]  # Chain code
        xprv += b"\x00" + seed[:32]  # Master key

        # Double hash using SHA256
        hashed_xprv = hashlib.sha256(xprv).digest()
        hashed_xprv = hashlib.sha256(hashed_xprv).digest()

        # Append 4 bytes of checksum
        xprv += hashed_xprv[:4]

        # Return base58
        return b58encode(xprv)
#######YOINKED CODE########################

a = '0488B21E'
b = '0488B21E'
c = bytes.fromhex(a)
d = bytes.fromhex(b)
print(a)
print(b)
print(a+b)
print(bytes.fromhex('00'))

seed = pg.gen_seed(pg.find_words(pg.hash_entropy(pg.gen_entropy(128), 128)))
a = bytes.fromhex('b1680c7a6ea6ed5ac9bf3bc3b43869a4c77098e60195bae51a94159333820e125c3409b8c8d74b4489f28ce71b06799b1126c1d9620767c2dadf642cf787cf36')
#a = bytes.fromhex("000102030405060708090a0b0c0d0e0f")
generate_master_private_key(a)
#print(to_hd_master_key(seed))