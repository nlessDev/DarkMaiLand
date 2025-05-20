from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from Crypto.Cipher import AES
from Crypto.Hash import HMAC, SHA256
from .utils.exceptions import CryptoError
from .utils import logger
import os

class SMTPXCrypto:
    def __init__(self):
        self.private_key = None
        self.peer_public_key = None
        self.session_key = None
        self.hmac_key = None

    def generate_keys(self):
        try:
            self.private_key = ec.generate_private_key(ec.SECP521R1())
            return self.private_key.public_key().public_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PublicFormat.SubjectPublicKeyInfo
            )
        except Exception as e:
            logger.error(f"Key generation failed: {str(e)}")
            raise CryptoError("Key generation failed") from e

    def derive_keys(self, peer_public_key):
        try:
            self.peer_public_key = serialization.load_pem_public_key(peer_public_key)
            shared = self.private_key.exchange(ec.ECDH(), self.peer_public_key)
            
            hkdf = HKDF(
                algorithm=hashes.SHA512(),
                length=64,
                salt=None,
                info=b'smtpx-key-derivation'
            )
            keys = hkdf.derive(shared)
            self.session_key = keys[:32]
            self.hmac_key = keys[32:]
        except Exception as e:
            logger.error(f"Key derivation failed: {str(e)}")
            raise CryptoError("Key exchange failed") from e

    def encrypt(self, data):
        try:
            cipher = AES.new(self.session_key, AES.MODE_GCM)
            ciphertext, tag = cipher.encrypt_and_digest(data)
            return cipher.nonce + tag + ciphertext
        except Exception as e:
            logger.error(f"Encryption failed: {str(e)}")
            raise CryptoError("Encryption failed") from e

    def decrypt(self, encrypted):
        try:
            nonce = encrypted[:16]
            tag = encrypted[16:32]
            ciphertext = encrypted[32:]
            cipher = AES.new(self.session_key, AES.MODE_GCM, nonce=nonce)
            return cipher.decrypt_and_verify(ciphertext, tag)
        except Exception as e:
            logger.error(f"Decryption failed: {str(e)}")
            raise CryptoError("Decryption failed") from e

    def generate_hmac(self, data):
        try:
            h = HMAC.new(self.hmac_key, digestmod=SHA256)
            h.update(data)
            return h.digest()
        except Exception as e:
            logger.error(f"HMAC generation failed: {str(e)}")
            raise CryptoError("HMAC failed") from e
