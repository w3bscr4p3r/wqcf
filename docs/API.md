# API contract (MVP)

Base path: `/v1`. JSON fields carrying binary data use standard Base64.

| Method | Endpoint | Purpose |
|---|---|---|
| GET | `/health` | Liveness |
| GET | `/v1/capabilities` | Runtime provider/algorithm discovery |
| POST | `/v1/kem/ml-kem-768/keypair` | Demo public-key generation |
| POST | `/v1/kem/ml-kem-768/encapsulate` | Demo encapsulation |
| POST | `/v1/aead/aes-256-gcm/encrypt` | AEAD encryption |
| POST | `/v1/signatures/ml-dsa-65/verify` | Signature verification |
| POST | `/v1/signatures/ml-dsa-65/sign` | Reserved; returns 501 until KMS/HSM key references exist |

Bearer authentication is enabled when `WQCF_API_TOKEN` is configured. Production deployments must fail closed and must use an external identity provider, scoped authorization and TLS/mTLS.

**MVP warning:** the demo encapsulation endpoint returns a shared secret to facilitate local interoperability testing. This is deliberately unsuitable for production. Production APIs must keep secrets server-side and expose only key references and ciphertext.
