import phrasegenerator as pg
import key_derivation as kd
import hash_collection as ha
import hashlib
import bitcoin
import base58


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


pub_key = '032c70b5429acab5b9f1822b94bdf062f3aea39e282fbc1af71a158d98b4f67a6a'
pub_key = bytes.fromhex(pub_key)
hashed256 = ha.sha256(pub_key).digest()
hashed160 = ha.ripemd160(hashed256).digest()
hashed160v = bytes.fromhex('00') + hashed160  # 00 for mainnet bitcoin
b58_hashed256_1 = ha.sha256(hashed160v).digest()
b58_hashed256_2 = ha.sha256(b58_hashed256_1).digest()
address_checksum = b58_hashed256_2[:4]
bin_btc_address = hashed160v + address_checksum
address = base58.b58encode(bin_btc_address)

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