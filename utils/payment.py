import json
import uuid
import time
import hashlib
import base64

from ecdsa import SigningKey
from ecdsa.util import sigencode_der
from django.conf import settings
bundle_id = 'com.sprinttech.hooked'
# key_id = 'XWSXTGQVX2'
key_id="ac058d10-2ebb-4c4b-b563-3e58f0d27c19"
product = 'profile_boost_1_month'
offer = 'discounter' # This is the code set in ASC
application_username = 'user_name' # Should be the same you use when
                                   # making purchases
def generateSignatures():
    nonce = uuid.uuid4()
    timestamp = int(round(time.time() * 1000))

    payload = '\u2063'.join([bundle_id, 
                            key_id, 
                            product, 
                            offer, 
                            application_username, 
                            str(nonce), # Should be lower case
                            str(timestamp)])

    # Read the key file
    with open(settings.BASE_DIR.joinpath('utils/cert.der'), 'rb') as myfile:
        der = myfile.read()

        signing_key = SigningKey.from_der(der)

        signature = signing_key.sign(payload.encode('utf-8'), 
                                    hashfunc=hashlib.sha256, 
                                    sigencode=sigencode_der)
        encoded_signature = base64.b64encode(signature)

    print(str(encoded_signature, 'utf-8'), str(nonce), str(timestamp), key_id)
    return {
        "signature": str(encoded_signature, 'utf-8'),
        "nonce": str(nonce),
        "timestamp": str(timestamp),
        "key_id": key_id,
        "payload": payload,
        "bundle_id": bundle_id,
        "product": product,
        "offer": offer,
        "application_username": application_username,
        "timestamp_ms": str(timestamp) 
    }