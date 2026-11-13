import base64
import os
import secrets
from fastapi import FastAPI, Header, HTTPException
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from .schemas import KEMEncapsulateRequest, EncryptRequest, SignRequest, VerifyRequest
from .provider import provider, ProviderUnavailable, _b64d, _b64e

app = FastAPI(
    title="WQCF API",
    version="0.1.0",
    description="WOLF Quantum-Safe Cryptographic Foundation — experimental MVP"
)

def require_auth(authorization: str | None):
    expected = os.getenv("WQCF_API_TOKEN", "")
    if not expected:
        if os.getenv("WQCF_ENV", "development") != "development":
            raise HTTPException(503, "API authentication is not configured")
        return
    supplied = authorization.removeprefix("Bearer ").strip() if authorization else ""
    if not secrets.compare_digest(supplied, expected):
        raise HTTPException(401, "Invalid bearer token")

def get_provider():
    try:
        return provider()
    except ProviderUnavailable as exc:
        raise HTTPException(503, str(exc))

@app.get("/health")
def health():
    return {"status": "ok", "service": "wqcf-api", "version": "0.1.0"}

@app.get("/v1/capabilities")
def capabilities():
    try:
        p = provider()
        return {"status": "available", **p.capabilities()}
    except ProviderUnavailable as exc:
        return {"status": "disabled", "provider": None, "reason": str(exc),
                "algorithms": {"kem": [], "signatures": []}}

@app.post("/v1/kem/ml-kem-768/keypair")
def kem_keypair(authorization: str | None = Header(default=None)):
    require_auth(authorization)
    p = get_provider()
    public, _private = p.kem_keypair()
    return {"algorithm": "ML-KEM-768", "public_key": public,
            "warning": "Demo only: private key custody is not implemented; do not use for real data."}

@app.post("/v1/kem/ml-kem-768/encapsulate")
def kem_encapsulate(body: KEMEncapsulateRequest, authorization: str | None = Header(default=None)):
    require_auth(authorization)
    p = get_provider()
    ciphertext, secret = p.kem_encapsulate(body.public_key)
    return {"algorithm": body.algorithm, "ciphertext": ciphertext,
            "shared_secret": secret,
            "warning": "Demo only: shared secret is exposed for interoperability testing; never expose it in production APIs."}

@app.post("/v1/aead/aes-256-gcm/encrypt")
def encrypt(body: EncryptRequest, authorization: str | None = Header(default=None)):
    require_auth(authorization)
    key, plaintext = _b64d(body.key_b64), _b64d(body.plaintext_b64)
    aad = _b64d(body.associated_data_b64) if body.associated_data_b64 else None
    if len(key) != 32:
        raise HTTPException(400, "AES-256-GCM requires a 32-byte key")
    nonce = secrets.token_bytes(12)
    ciphertext = AESGCM(key).encrypt(nonce, plaintext, aad)
    return {"algorithm": "AES-256-GCM", "nonce_b64": _b64e(nonce),
            "ciphertext_b64": _b64e(ciphertext)}

@app.post("/v1/signatures/ml-dsa-65/verify")
def verify(body: VerifyRequest, authorization: str | None = Header(default=None)):
    require_auth(authorization)
    p = get_provider()
    try:
        valid = p.verify(_b64d(body.message_b64), _b64d(body.signature_b64), _b64d(body.public_key_b64))
    except ValueError as exc:
        raise HTTPException(400, str(exc))
    return {"algorithm": body.algorithm, "valid": valid}

@app.post("/v1/signatures/ml-dsa-65/sign")
def sign(body: SignRequest, authorization: str | None = Header(default=None)):
    require_auth(authorization)
    raise HTTPException(501, "Signing endpoint requires an HSM/KMS-backed key reference. Raw private-key signing is intentionally not exposed in this MVP.")
