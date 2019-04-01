from Crypto.Cipher import AES
from Crypto.Util import Counter
from Crypto import Random
import binascii
import codecs
key_bytes = 32

def encrypt(key, plaintext):
    assert len(key) == key_bytes

    iv = Random.new().read(AES.block_size)

    iv_int = int(binascii.hexlify(iv), 16) 

    ctr = Counter.new(AES.block_size * 8, initial_value=iv_int)

    aes = AES.new(key, AES.MODE_CTR, counter=ctr)

    ciphertext = aes.encrypt(plaintext)
    return (iv, ciphertext)


def decrypt(key, iv, ciphertext):
    assert len(key) == key_bytes

    iv_int = int(codecs.encode(iv,'hex'), 16) 
    ctr = Counter.new(AES.block_size * 8, initial_value=iv_int)

    aes = AES.new(key, AES.MODE_CTR, counter=ctr)

    plaintext = aes.decrypt(ciphertext)
    return plaintext

key='D81C52F524F6FAF198B5DAA2A865C2DF'
(iv, ciphertext) = encrypt(key, 'TestText')
print(decrypt(key, iv, ciphertext))
#d=decrypt(key, iv, ciphertext)
