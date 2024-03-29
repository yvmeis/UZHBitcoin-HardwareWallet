import btclib
from . import phrasegenerator as pg
from . import key_derivation as kd
from . import hash_collection as hc
import btclib.dsa
import btclib.bip32
from btclib.bip32 import _BIP32KeyData
from dataclasses_json import DataClassJsonMixin, config


def sign_tx(tx_data: str, priv_key: bytes):
    """creates the R and S values, given the transaction data and the private key"""
    
    if isinstance(tx_data, bytes):
        m = tx_data.decode('utf8')
    elif isinstance(tx_data, str):
        m = tx_data

        
    signature = btclib.dsa.sign(m, priv_key)
    
    return signature


def serialize_tx(r: int, s: int, sighash_suffix = '01') -> str:
    """creates a serialized signature out of the R and S values. Can accept different sighash suffixes"""
    
    r = hex(r)[2:]
    r = r.zfill(64)
    r_byte = bytes.fromhex(r)
    
    s = hex(s)[2:]
    s = s.zfill(64)
    s_byte = bytes.fromhex(s)
    
    length_r = hex(len(r_byte))[2:]
    length_s = hex(len(s_byte))[2:]
    
    DER_start = '30'
    sequence_length = str(int(length_r) + int(length_s) + 4)
    
    integer_value_indicator = '02'

    serialized_signature = DER_start + sequence_length + integer_value_indicator + length_r + r + integer_value_indicator + length_s + s + sighash_suffix
    
    return serialized_signature
    

def scriptSig_serialization(serialized_signature: str, pub_key: bytes) -> str:
    """creates the script Sig serialization out of a serialized signature and the public key"""
    
    sig_byte = bytes.fromhex(serialized_signature)
    sig_length = hex(len(sig_byte))[2:]
    #pub_byte = bytes.fromhex(pub_key)
    pub_key_length = hex(len(pub_key.key))[2:]
    
    scriptSig = sig_length + serialized_signature + pub_key_length + pub_key.key.hex()
    return scriptSig
    

def gen_ephemeral_priv_key() -> bytes:  
    """generates a temporary private key"""
    
    ephemeral_priv_key = kd.serialize(kd.generate_master_private_key(pg.gen_seed(pg.find_words(pg.hash_entropy(pg.gen_entropy(128), 128)))), prv_pbl='private', derivation_level='00')
    
    return ephemeral_priv_key


def gen_ephemeral_key_pair(priv_key: bytes) -> tuple:
    """generates a temporary public key"""
    
    ephemeral_pub_key = kd.prv_to_pub(priv_key)
    
    return (priv_key, ephemeral_pub_key)


def signing(ephemeral_key_pair: tuple, signing_priv_key: bytes, transaction_data: str, prime_order_EC = int('FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141', 16)) -> tuple:
    """DO NOT RUN!! This function is a work in progress!!"""
    
    R = kd.get_x_point_from_key(ephemeral_key_pair[1])
    
    S = create_S(ephemeral_key_pair[0], R, signing_priv_key, transaction_data, prime_order_EC)
    
    return (R, S)


def create_S(ephemeral_priv_key: bytes, x_point: int, signing_priv_key: bytes, transaction_data: str, prime_order_EC: int) -> float:
    """DO NOT RUN!! This function is a work in progress!!    k-1 (Hash(m) + dA * R) mod n"""    
    
    hashm = int(hc.sha256(transaction_data.encode('utf8')).hexdigest(), 16)
    k1 = int.from_bytes(ephemeral_priv_key, 'big')**(-1)
    dA = int.from_bytes(signing_priv_key, 'big')
    S1 = (hashm + dA * x_point)
    S = k1 *S1 % prime_order_EC
    
    return S


def deserialize(key: bytes):
    """deserializes a key"""
    
    décodée = btclib.bip32.BIP32KeyData.b58decode(key)
    return décodée
