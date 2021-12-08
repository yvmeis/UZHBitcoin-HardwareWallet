#from . 
import phrasegenerator as pg
import base58
import bitcoin
#from . 
import hash_collection as ha
from btclib import to_pub_key
from btclib.curve import secp256k1
import btclib
from btclib import *
import address_gen


def generate_master_private_key(seed):  # seed as a bytestring
    key = "Bitcoin seed"
    key = key.encode(encoding='UTF-8')
    h = ha.hmacsha256(key, seed).digest()
    master_private_key = h[:32]
    chain_code = h[32:]
    extended_master_private_key = (master_private_key, chain_code)
    return extended_master_private_key


def serialize(extended_key: tuple, prv_pbl: str, derivation_level: str, net='mainnet', fingerprint='00000000', childnumber='00000000'):
    '''remove '0x' from all hex strings'''
    # extended_key: tuple with [0] = TYPE BYTE: key, [1] = TYPE BYTE: chain code
    # prv_bl = TYPE STRING: 'private'/'public';
    # derivation_level = TYPE HEXSTRING: 0x00 for master, 0x01 for level-1 derived, ...
    # net = TYPE STRING: 'mainnet'/'testnet'
    # fingerprint = TYPE HEXSTRING: 0x00000000 for master, fingerprint of the parent's key for children
    # childnumber = TYPE HEXSTRING: 0x00000000 for master, ??? for children

    specs = {'mainnet': {'public': '0488B21E', 'private': '0488ADE4'}, 'testnet': {'public': '043587CF', 'private': '04358394'},
             }

    serialized_key = bytes.fromhex(specs[net][prv_pbl])
    serialized_key += bytes.fromhex(derivation_level)
    serialized_key += bytes.fromhex(fingerprint)

    if derivation_level == '00':
        serialized_key += bytes.fromhex(childnumber)  # for master
    if derivation_level != '00':
        pass  # children: still to be done
    serialized_key += extended_key[1]

    if prv_pbl == 'private':
        serialized_key += bytes.fromhex('00') + extended_key[0]
    if prv_pbl == 'public':
        pass  # public key: still to be done

    hashed_serialized_key = ha.sha256(serialized_key).digest()
    hashed_serialized_key = ha.sha256(hashed_serialized_key).digest()

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
    #pub = bitcoin.bip32_privtopub(prv_key)
    pub = btclib.bip32.xpub_from_xprv(prv_key)
    return pub

#kaputt
'''
def gen_address(pub_key):
    pub_key = bitcoin.bip32_deserialize(pub_key)[-1]
    pub_key = pub_key.hex()
    pub_key = str(pub_key)
    if isinstance(pub_key, str):
        print(pub_key)
    pub_key = bytes.fromhex(pub_key)
    hashed256 = ha.sha256(pub_key).digest()
    hashed160 = ha.ripemd160(hashed256).digest()
    hashed160v = bytes.fromhex('00') + hashed160  # 00 for mainnet bitcoin
    b58_hashed256_1 = ha.sha256(hashed160v).digest()
    b58_hashed256_2 = ha.sha256(b58_hashed256_1).digest()
    address_checksum = b58_hashed256_2[:4]
    bin_btc_address = hashed160v + address_checksum
    address = base58.b58encode(bin_btc_address)
    

    return address
'''

def get_y_point_from_key(pub):
    point = to_pub_key._point_from_xpub(pub, secp256k1)
    return point[1]


def get_x_point_from_key(pub):
    point = to_pub_key._point_from_xpub(pub, secp256k1)
    return point[0]


def gen_as_dictionary():
    seed_phrase = pg.find_words(pg.hash_entropy(pg.gen_entropy(128), 128))
    priv_key = serialize(generate_master_private_key(pg.gen_seed(seed_phrase)), prv_pbl='private', derivation_level='00')
    address =  address_gen.gen_address(prv_to_pub(priv_key))
    
    dic = {'seed_phrase': seed_phrase, 'private_key': priv_key, 'address': address}
    
    return dic   

def gen_wallet():
    # TODO generate wallet information
    pvt_key = "blabla"
    seed_phrase = "banana apple ..."
    addr = "someaddress"

    return {
        "pvt_key": pvt_key,
        "seed_phrase": seed_phrase,
        "addr": addr
    }

