"""

Yubikey decrypting and parsing library

"""
import re

from aes import aes_decrypt

RE_TOKEN = re.compile(r'^[cbdefghijklnrtuv]{32,64}$')
RE_AES_KEY = re.compile(r'^[0-9a-fA-F]{32}$')

class InvalidToken(Exception):
    pass

class InvalidAESKey(Exception):
    pass

class YubikeyToken:

    def __init__(self, input, aes_key):

        if not RE_TOKEN.match(input):
            raise InvalidToken('Invalid token. A token should be 34 to 64 ModHex characters.')

        if not RE_AES_KEY.match(aes_key):
            raise InvalidAESKey('Invalid AES key. The key should be 32 hexadecimal characters.')

        self.public_id = input[:-32]
        self.token = input[-32:]
        self.aes_key = aes_key
        
        token_bin = ''.join(modhex_decode(self.token))

        aes_key_bin = self.aes_key.decode('hex')
        decoded = aes_decrypt(token_bin, aes_key_bin)

        self.secret_id = decoded[0:6].encode('hex')
        self.counter = ord(decoded[7]) * 256 + ord(decoded[6])
        self.timestamp = ord(decoded[10]) * 65536 + ord(decoded[9]) * 256 + ord(decoded[8])
        self.counter_session = ord(decoded[11])
        self.random_number = ord(decoded[13]) * 256 + ord(decoded[12])
        self.crc = ord(decoded[15]) * 256 + ord(decoded[14])
        self.crc_ok = crc_check(decoded)

    def __str__(self):
        return 'Key for ID %s' % self.public_id
 
def modhex_decode(input):
    it = iter(input)
    chars = 'cbdefghijklnrtuv'
    for first, second in zip(it, it):
        yield chr(chars.index(first) * 16 + chars.index(second))

def crc_check(decoded):
    m_crc = 0xffff
    for pos in range(0, 16):
        m_crc ^= ord(decoded[pos]) & 0xff
        for i in range(0, 8):
            test = m_crc & 1
            m_crc >>= 1
            if test:
                m_crc ^= 0x8408

    return m_crc == 0xf0b8
