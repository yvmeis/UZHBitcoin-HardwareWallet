import phrasegenerator as pg
import key_derivation as kd
import bitcoin

entropy = pg.hash_entropy(pg.gen_entropy(128), 128)
words = pg.find_words(entropy)
seed = pg.gen_seed(words)
master = kd.serialize(kd.generate_master_private_key(
    seed), prv_pbl='private', derivation_level='00')
print(entropy[:-4])
print(words)
print(seed.hex())
der = kd.derive_child(master, 0)
print('child 1 private: ' + der)
print('child 1 public: ' + kd.prv_to_pub(der))
der_2 = kd.derive_child(der, 0)
print('child 2 private: ' + der_2)
pub = kd.prv_to_pub(der_2)
pub2 = bitcoin.bip32_deserialize(pub)[-1]
pub2 = pub2.hex()
print('child 2 public: ' + pub2)
address = kd.gen_address(pub)
print('child 2 address(byte): ' + str(address))
print('child 2 address(hex): ' + address.hex())
