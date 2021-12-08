import btclib
import json
import btclib.psbt, btclib.psbt_in, btclib.tx, btclib.tx_in, btclib.psbt_in, btclib.psbt_out
import btclib.tests.generated_files
from btclib.psbt import *
import signer as sig


def psbt_64_decoder(b64_psbt):
    psbt = Psbt.b64decode(b64_psbt)
    assert psbt.b64encode() == b64_psbt
    
    return psbt

def finalize(psbt):
    f_psbt = finalize_psbt(psbt)

    return f_psbt

#privkey in form: (03 572f9af6aebd7a6764264e17abdc4fc80cf359c11f81cbbe4ecf7a2c234a5f8f)
#sig in serialized form
def _sign_psbt(psbt, priv_key, signature):
    psbt.inputs[0].partial_sigs[priv_key] = signature
    assert psbt.inputs[0].partial_sigs[priv_key] == signature
    
def sign_psbt(psbt, priv_key):
    tx_data = psbt_to_tx(psbt)
    signature = sig.sign_tx(tx_data, priv_key)
    serialized_signature = sig.serialize_tx(signature.r, signature.s)
    signed_psbt = _sign_psbt(psbt, priv_key, serialized_signature)
    return signed_psbt

def psbt_to_tx(psbt):
    return 'test'

def psbt_64_encoder(psbt):
    encoded_psbt = psbt.b64encode()
    return encoded_psbt

############TESTS#############
psbt_tx_b64 ='cHNidP8BAHUCAAAAASaBcTce3/KF6Tet7qSze3gADAVmy7OtZGQXE8pCFxv2AAAAAAD+////AtPf9QUAAAAAGXapFNDFmQPFusKGh2DpD9UhpGZap2UgiKwA4fUFAAAAABepFDVF5uM7gyxHBQ8k0+65PJwDlIvHh7MuEwAAAQD9pQEBAAAAAAECiaPHHqtNIOA3G7ukzGmPopXJRjr6Ljl/hTPMti+VZ+UBAAAAFxYAFL4Y0VKpsBIDna89p95PUzSe7LmF/////4b4qkOnHf8USIk6UwpyN+9rRgi7st0tAXHmOuxqSJC0AQAAABcWABT+Pp7xp0XpdNkCxDVZQ6vLNL1TU/////8CAMLrCwAAAAAZdqkUhc/xCX/Z4Ai7NK9wnGIZeziXikiIrHL++E4sAAAAF6kUM5cluiHv1irHU6m80GfWx6ajnQWHAkcwRAIgJxK+IuAnDzlPVoMR3HyppolwuAJf3TskAinwf4pfOiQCIAGLONfc0xTnNMkna9b7QPZzMlvEuqFEyADS8vAtsnZcASED0uFWdJQbrUqZY3LLh+GFbTZSYG2YVi/jnF6efkE/IQUCSDBFAiEA0SuFLYXc2WHS9fSrZgZU327tzHlMDDPOXMMJ/7X85Y0CIGczio4OFyXBl/saiK9Z9R5E5CVbIBZ8hoQDHAXR8lkqASECI7cr7vCWXRC+B3jv7NYfysb3mk6haTkzgHNEZPhPKrMAAAAAAAAA'
psbt = psbt_64_decoder(psbt_tx_b64)
priv_key = bytes.fromhex('03 572f9af6aebd7a6764264e17abdc4fc80cf359c11f81cbbe4ecf7a2c234a5f8f')
signature = bytes.fromhex('3045022100e1ea1a3f9f790492eb18810f0e49e650b3397f91fa4a380c0649e3144943009e02202c36df002e2d1b211da0256b446b27541e330c46fd9386b59a161b4902e854cb01')
print(psbt)
print()
_sign_psbt(psbt, priv_key, signature)
print(psbt)
print()

f_psbt = finalize(psbt)
print(f_psbt)
print()
print(psbt_64_encoder(f_psbt))