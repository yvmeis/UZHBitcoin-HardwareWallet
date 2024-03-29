from . import key_derivation as kd
from . import hash_collection as hc

def verify_signature(R: int, S: int, signing_pub_key: bytes, transaction_data: str, EC_generator_point) -> bool:
    """ verifies if a signature is valid """
    
    P = (S**(-1)) * hc.sha256(transaction_data) * EC_generator_point + (S**(-1)) * R * signing_pub_key
    
    P_x_point= kd.get_x_point_from_key(P)
    
    if R == P_x_point:
        return True
    else:
        return False
    