# Threat model (initial)

## Assets
- Private signing and decapsulation keys.
- Shared secrets and derived AEAD keys.
- Plaintext and ciphertext.
- Identity credentials, API tokens, audit metadata.

## Threat actors
- Network attacker; compromised client; malicious tenant; insider; compromised host/container; supply-chain attacker; future cryptanalytic capability.

## Primary controls
- TLS 1.3 or stronger deployment baseline; mTLS for internal service calls.
- KMS/HSM custody, least privilege, rotation and revocation.
- Authentication and per-operation authorization.
- Rate limiting, request size limits, replay controls and audit trails.
- Dependency pinning, SBOM, signed builds, reproducible build goals and vulnerability scanning.
- No secrets/plaintext in logs, traces, exceptions or metrics.
- Cryptographic agility with explicit algorithm allowlists and versioned envelopes.

## Out of scope for this MVP
- FIPS 140 validation; production KMS/HSM integration; formal verification; multi-tenant isolation certification; production hybrid protocol; side-channel certification.
