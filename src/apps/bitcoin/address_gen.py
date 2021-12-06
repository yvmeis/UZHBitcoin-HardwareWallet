
import hash_collection as ha
import hashlib
import bitcoin
import base58




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
    address = base58.b58encode(bin_btc_address)
    print(address)
    return address
    