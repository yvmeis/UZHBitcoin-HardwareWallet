from btclib import *
import phrasegenerator as pg
import key_derivation as kd
import hash_collection as hc

def create_S(ephemeral_priv_key, x_point, signing_priv_key, transaction_data, prime_order_EC):
    #' k-1 (Hash(m) + dA * R) mod n'
    S = (ephemeral_priv_key**(-1)) * (hc.sha256(transaction_data) + (signing_priv_key * x_point)) % prime_order_EC
    
    return S

def gen_ephemeral_priv_key():  
    ephemeral_priv_key = kd.serialize(kd.generate_master_private_key(pg.gen_seed(pg.find_words(pg.hash_entropy(pg.gen_entropy(128), 128)))), prv_pbl='private', derivation_level='00')
    
    return ephemeral_priv_key

def gen_ephemeral_key_pair(priv_key):
    ephemeral_pub_key = kd.prv_to_pub(priv_key)
    
    return (priv_key, ephemeral_pub_key)

def sign(ephemeral_key_pair, signing_priv_key, transaction_data, prime_order_EC):
    
    R = kd.get_x_point_from_key(ephemeral_key_pair[1])
    
    S = create_S(ephemeral_key_pair[0], R, signing_priv_key, transaction_data, prime_order_EC)
    
    return (R, S)

print(gen_ephemeral_priv_key())