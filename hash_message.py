import hashlib

def to_hash(message):
    message = message.encode('utf-8')
    sha3_512 = hashlib.sha3_512(message)
    sha3_512_hex_digest = sha3_512.hexdigest()
    return sha3_512_hex_digest
