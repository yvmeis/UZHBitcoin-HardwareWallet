import phrasegenerator as pg
import key_derivation as kd
import hash_collection as ha
import hashlib
import bitcoin

'''
entropy = pg.hash_entropy(pg.gen_entropy(128), 128)
words = pg.find_words(entropy)
seed = pg.gen_seed(words)
master = kd.serialize(kd.generate_master_private_key(
    seed), prv_pbl='private', derivation_level='00')
print(entropy[:-4])
print(words)
print(seed.hex())
der = kd.derive_child(master, 0)
der_2 = kd.derive_child(der, 0)
pub = kd.prv_to_pub(der_2)
pub2 = bitcoin.bip32_deserialize(pub)[-1]
pub2 = pub2.hex()
print('child 2 public: ' + pub2)
address = kd.gen_address(pub)
print('child 2 address(byte): ' + str(address))
'''

pub_key = '0250863ad64a87ae8a2fe83c1af1a8403cb53f53e486d8511dad8a04887e5b2352'
#pub_key = bitcoin.bip32_deserialize(pub_key)[-1]
#pub_key = pub_key.hex()
pub_key = bytes.fromhex(pub_key)
hashed256 = ha.sha256(pub_key).digest()
print(hashed256.hex())
hashed160 = ha.ripemd160(hashed256).digest()
print(hashed160.hex())
hashed160v = bytes.fromhex('00') + hashed160  # 00 for mainnet bitcoin
print(hashed160v.hex())
b58_hashed256_1 = ha.sha256(hashed160v).digest()
print(b58_hashed256_1.hex())
b58_hashed256_2 = ha.sha256(b58_hashed256_1).digest()
print(b58_hashed256_2.hex())
address_checksum = b58_hashed256_2[:4]
print(address_checksum.hex())
bin_btc_address = hashed160v + address_checksum
print(bin_btc_address.hex())
address = kd.encode_b58(bin_btc_address)
print(address)


'''
hashed256 = ha.sha256(pub_key).digest()
hashed160 = ha.ripemd160(hashed256).digest()
hashed160v = bytes.fromhex('00') + hashed160  # 00 for mainnet bitcoin
b58_hashed256_1 = ha.sha256(hashed160v).digest()
b58_hashed256_2 = ha.sha256(b58_hashed256_1).digest()
address_checksum = b58_hashed256_2[:4]
bin_btc_address = hashed160v + address_checksum
address = encode_b58(bin_btc_address)


def gen_address(pub_key):
    pub_key = bitcoin.bip32_deserialize(pub_key)[-1]
    pub_key = pub_key.hex()
    pub_key = bytes.fromhex(pub_key)
    hashed256 = ha.sha256(pub_key).digest()
    hashed160 = ha.ripemd160(hashed256).digest()
    hashed160v = bytes.fromhex('00') + hashed160  # 00 for mainnet bitcoin
    b58_hashed256_1 = ha.sha256(hashed160v).digest()
    b58_hashed256_2 = ha.sha256(b58_hashed256_1).digest()
    address_checksum = b58_hashed256_2[:4]
    bin_btc_address = hashed160v + address_checksum
    address = encode_b58(bin_btc_address)
    return address
'''