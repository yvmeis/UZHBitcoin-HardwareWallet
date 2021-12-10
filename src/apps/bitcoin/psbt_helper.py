import btclib
import json
import btclib.psbt, btclib.psbt_in, btclib.tx, btclib.tx_in, btclib.psbt_in, btclib.psbt_out
import btclib.tests.generated_files
from btclib.psbt import *
from . import signer as sig


def psbt_64_decoder(b64_psbt) -> Psbt:
    """converts the psbt form base 64"""
    
    psbt = Psbt.b64decode(b64_psbt)
    assert psbt.b64encode() == b64_psbt
    
    return psbt


def psbt_64_encoder(psbt: Psbt):
    """ encodes a psbt into base 64 form """
    
    encoded_psbt = psbt.b64encode()
    return encoded_psbt


def finalize(psbt: Psbt) -> Psbt:
    """finalizes a psbt"""
    
    f_psbt = finalize_psbt(psbt)

    return f_psbt


def _sign_psbt(psbt: Psbt, priv_key:str, signature: str):
    """ 
    puts the signature into the corresponding spot in the psbt;
    privkey in form: (03 572f9af6aebd7a6764264e17abdc4fc80cf359c11f81cbbe4ecf7a2c234a5f8f);
    sig in serialized form 
    """
    
    psbt.inputs[0].partial_sigs[priv_key] = signature
    assert psbt.inputs[0].partial_sigs[priv_key] == signature
    
    
def sign_psbt(psbt: Psbt, priv_key: bytes) -> Psbt:
    """the function to be used from the outside. This function takes a psbt and a private key and returns a signed psbt"""
    
    tx_data = psbt_to_tx(psbt)
    signature = sig.sign_tx(tx_data, priv_key)
    serialized_signature = sig.serialize_tx(signature.r, signature.s)
    _sign_psbt(psbt, priv_key, serialized_signature)
    finalized_psbt = finalize(psbt)
    return finalized_psbt


def psbt_to_tx(psbt: Psbt) -> str:
    """Work in progress!! This function should extract the transaction data from a psbt"""
    
    return 'test'
