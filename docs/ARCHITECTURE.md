# Architecture

## Logical layers

1. Language SDKs (PHP, Node.js, future Python/Java/Go).
2. API gateway: transport, authentication, authorization, quotas, request validation.
3. Python orchestration: provider discovery, policy selection, audit events and workflow composition.
4. Rust core: shared types, policy validation and future native provider boundary.
5. Cryptographic provider: maintained PQC implementation; never handwritten primitives.
6. Key custody: external KMS/HSM, ideally non-exportable keys.
7. Persistence/observability: metadata and audit records only; never persist plaintext or raw private keys by default.

## Data protection flow

Sender obtains a recipient ML-KEM-768 public key, encapsulates a shared secret, derives an AEAD key using HKDF-SHA-384 with protocol context, and encrypts payloads with AES-256-GCM using a unique 96-bit nonce. Recipient decapsulates and derives the same AEAD key before authenticated decryption.

The production protocol must define transcript binding, context separation, replay protection, key identifiers, version negotiation, nonce policy and error handling. Use a reviewed protocol design rather than inventing a hybrid combiner.

## Hybrid transition

Hybrid key establishment is a protocol property, not a checkbox. Define the classical component, PQC component, combiner/KDF, downgrade resistance, transcript binding, negotiation and failure semantics. Have the construction independently reviewed before production.
