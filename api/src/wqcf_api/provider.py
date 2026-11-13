import base64
import os

class ProviderUnavailable(RuntimeError):
    pass

def _b64d(value: str) -> bytes:
    try:
        return base64.b64decode(value, validate=True)
    except Exception as exc:
        raise ValueError("Invalid base64 input") from exc

def _b64e(value: bytes) -> str:
    return base64.b64encode(value).decode("ascii")

class OQSProvider:
    """Thin adapter for liboqs-python. Requires a separately installed native liboqs."""

    def __init__(self):
        if os.getenv("WQCF_PROVIDER", "disabled").lower() != "oqs":
            raise ProviderUnavailable("PQC provider is disabled")
        try:
            import oqs
        except Exception as exc:
            raise ProviderUnavailable("liboqs-python/liboqs is not available") from exc
        self.oqs = oqs

    def capabilities(self):
        try:
            kem = self.oqs.get_enabled_kem_mechanisms()
            sig = self.oqs.get_enabled_sig_mechanisms()
        except Exception as exc:
            raise ProviderUnavailable("Unable to query OQS provider") from exc
        return {
            "provider": "liboqs",
            "kem": [x for x in kem if x == "ML-KEM-768"],
            "signatures": [x for x in sig if x in ("ML-DSA-65", "SLH-DSA-SHA2-128s")],
        }

    def kem_keypair(self):
        with self.oqs.KeyEncapsulation("ML-KEM-768") as kem:
            public = kem.generate_keypair()
            secret = kem.export_secret_key()
        # Private key is intentionally not returned or persisted by this demo API.
        return _b64e(public), _b64e(secret)

    def kem_encapsulate(self, public_key_b64):
        public = _b64d(public_key_b64)
        with self.oqs.KeyEncapsulation("ML-KEM-768") as kem:
            ciphertext, shared_secret = kem.encap_secret(public)
        return _b64e(ciphertext), _b64e(shared_secret)

    def sign_keypair(self):
        with self.oqs.Signature("ML-DSA-65") as sig:
            public = sig.generate_keypair()
            secret = sig.export_secret_key()
        return _b64e(public), _b64e(secret)

    def sign(self, message: bytes, secret_key: bytes):
        with self.oqs.Signature("ML-DSA-65", secret_key=secret_key) as sig:
            return sig.sign(message)

    def verify(self, message: bytes, signature: bytes, public_key: bytes):
        with self.oqs.Signature("ML-DSA-65") as sig:
            return bool(sig.verify(message, signature, public_key))

def provider():
    return OQSProvider()
