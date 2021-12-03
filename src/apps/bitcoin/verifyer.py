from btclib import *
import phrasegenerator as pg
import key_derivation as kd
import hash_collection as hc

def verify_signature(R, S, signing_pub_key, transaction_data, EC_generator_point):
    P = (S**(-1)) * hc.sha256(transaction_data) * EC_generator_point + (S**(-1)) * R * signing_pub_key
    
    x_of_P = kd.get_x_point_from_key(P)
    
    
    