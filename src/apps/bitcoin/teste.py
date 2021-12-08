import phrasegenerator as pg
import key_derivation as kd
import hash_collection as ha
import hashlib
import bitcoin
import base58
import address_gen

entropy = pg.hash_entropy(pg.gen_entropy(128), 128)
words = pg.find_words(entropy)
seed = pg.gen_seed(words)
master = kd.serialize(kd.generate_master_private_key(
    seed), prv_pbl='private', derivation_level='00')
print(type(master))
'''
print(entropy[:-4])
print(words)
print(seed.hex())
der = kd.derive_child(master, 0)
der_2 = kd.derive_child(der, 0)
pub = kd.prv_to_pub(der_2)
newpub = address_gen.gen_address(pub)
print('AAAAAAAAAAAA')
print(newpub)
pub2 = bitcoin.bip32_deserialize(pub)[-1]
pub2 = pub2.hex()
print('child 2 public: ' + pub2)
address = kd.gen_address(pub)
print('child 2 address(byte): ' + str(address))





print('BBBBBBBBBBB')
print(kd.gen_as_dictionary())
'''