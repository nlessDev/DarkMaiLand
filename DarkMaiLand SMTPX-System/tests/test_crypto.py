import pytest
from smtpx.crypto import SMTPXCrypto
from smtpx.utils.exceptions import CryptoError

class TestCrypto:
    @pytest.fixture
    def crypto(self):
        return SMTPXCrypto()

    def test_key_exchange(self, crypto):
        peer_crypto = SMTPXCrypto()
        crypto.derive_keys(peer_crypto.generate_keys())
        peer_crypto.derive_keys(crypto.generate_keys())
        
        test_data = b"Test message"
        encrypted = crypto.encrypt(test_data)
        decrypted = peer_crypto.decrypt(encrypted)
        
        assert decrypted == test_data

    def test_tampered_data(self, crypto):
        crypto.derive_keys(crypto.generate_keys())  # Self-signed for test
        encrypted = crypto.encrypt(b"Secret")
        
        # Tamper with HMAC
        with pytest.raises(CryptoError):
            crypto.decrypt(encrypted[:-5] + b"XXXXX")

    def test_empty_encryption(self, crypto):
        with pytest.raises(CryptoError):
            crypto.encrypt(b'')
