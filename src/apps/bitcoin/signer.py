import phrasegenerator as pg
import key_derivation as kd
import hash_collection as hc


def create_S(ephemeral_priv_key, x_point, signing_priv_key, transaction_data, prime_order_EC):
    #' k-1 (Hash(m) + dA * R) mod n'
    
    hashm = int(hc.sha256(transaction_data.encode('utf8')).hexdigest(), 16)
    k1 = int.from_bytes(ephemeral_priv_key, 'big')**(-1)
    dA = int.from_bytes(signing_priv_key, 'big')
    S1 = (hashm + dA * x_point)
    S2 = S1 % prime_order_EC
    S = k1 *S2
    
    return S

def gen_ephemeral_priv_key():  
    ephemeral_priv_key = kd.serialize(kd.generate_master_private_key(pg.gen_seed(pg.find_words(pg.hash_entropy(pg.gen_entropy(128), 128)))), prv_pbl='private', derivation_level='00')
    
    return ephemeral_priv_key

def gen_ephemeral_key_pair(priv_key):
    ephemeral_pub_key = kd.prv_to_pub(priv_key)
    
    return (priv_key, ephemeral_pub_key)

def sign(ephemeral_key_pair, signing_priv_key, transaction_data, prime_order_EC = int('FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141', 16)):
    
    R = kd.get_x_point_from_key(ephemeral_key_pair[1])
    
    S = create_S(ephemeral_key_pair[0], R, signing_priv_key, transaction_data, prime_order_EC)
    
    return (R, S)


###################TEST####################

print()
print()
print('Signer Testing')
print()
print()

print(sign(gen_ephemeral_key_pair(gen_ephemeral_priv_key()), kd.serialize(kd.generate_master_private_key(
    pg.gen_seed(pg.find_words(pg.hash_entropy(pg.gen_entropy(128), 128)))), prv_pbl='private', derivation_level='00'), '1 bitcoin from adam to badam'))

