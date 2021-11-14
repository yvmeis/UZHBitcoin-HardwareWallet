import os,binascii,bitcoin

def generate_entropy():
    hexstring = binascii.b2a_hex(os.urandom(16))
    return hexstring
    

def generate_recovery_phrases(hexstring):
    phrases = bip39.mnemonic_from_bytes(hexstring)

generate_recovery_phrases(generate_entropy)