# WQCF — WOLF Quantum-Safe Cryptographic Foundation

Open-source foundation for post-quantum cryptography (PQC), with a language-independent API, Python orchestration, a Rust policy/core crate, and PHP/Node.js SDKs.

> **Status: MVP scaffold / experimental. Not production-ready.** Cryptographic operations are enabled only when the optional Open Quantum Safe Python binding and its native `liboqs` dependency are correctly installed. This repository is not a validated cryptographic module and does not claim FIPS 140 validation.

## Goals

- Standardized PQC algorithms: ML-KEM-768 (FIPS 203), ML-DSA-65 (FIPS 204), and SLH-DSA (FIPS 205).
- Hybrid migration patterns and cryptographic agility.
- A stable REST/JSON contract for Python, PHP, Node.js and other languages.
- Separation of key encapsulation, key derivation, and authenticated data encryption.
- Auditable operations and explicit key-management boundaries.

## Repository layout

```text
wqcf/
├── api/                 # FastAPI service and provider adapter
├── core-rust/           # Rust policy/types crate (no handwritten crypto)
├── sdk/
│   ├── php/             # PHP SDK
│   └── node/            # TypeScript SDK
├── docs/                # Architecture, threat model, API and operations
├── examples/            # Integration examples
├── tests/               # API contract tests
├── deploy/              # Container deployment
├── .env.example
├── docker-compose.yml
└── LICENSE
```

## Quick start (API without PQC provider)

```bash
python -m venv .venv
. .venv/bin/activate
pip install -e ./api
uvicorn wqcf_api.main:app --host 127.0.0.1 --port 8080
```

OpenAPI: `http://127.0.0.1:8080/docs`

The service health and capability endpoints work without a crypto provider. Cryptographic endpoints fail closed with HTTP 503 until a supported provider is installed and configured.

## Enable the experimental OQS provider

Install a compatible `liboqs` native library and the matching `liboqs-python` binding according to the official Open Quantum Safe instructions. Then install the optional extra:

```bash
pip install -e './api[oqs]'
WQCF_PROVIDER=oqs uvicorn wqcf_api.main:app --host 127.0.0.1 --port 8080
```

Check `/v1/capabilities` before using operations. Provider names and algorithm identifiers are checked at runtime; do not assume availability from configuration alone.

## Rust crate

```bash
cd core-rust
cargo test
```

The Rust crate currently contains shared policy and type definitions. It deliberately does not implement cryptographic primitives. The next engineering milestone is a reviewed Rust provider adapter backed by a maintained PQC implementation, plus cross-language known-answer and interoperability tests.

## SDKs

PHP:
```php
require __DIR__ . '/../vendor/autoload.php';
$client = new Wqcf\Client('http://127.0.0.1:8080');
print_r($client->capabilities());
```

Node.js:
```ts
import { WqcfClient } from "@wolf/wqcf";
const client = new WqcfClient("http://127.0.0.1:8080");
console.log(await client.capabilities());
```

## Security boundaries

- Never expose private keys through API responses.
- Do not store production private keys in PostgreSQL, environment variables, source control, or container images.
- Use an HSM/KMS or a dedicated secrets boundary for production key custody.
- Terminate TLS at a trusted ingress; use mTLS for service-to-service communication.
- Authenticate callers, authorize each operation, rate-limit, and audit without logging secrets or plaintext.
- AES-GCM nonces must never repeat under the same key. The MVP generates a fresh random 96-bit nonce for each encryption request.
- KEM output is a shared secret, **not** an encryption key by itself. Derive purpose-specific keys with a KDF and use authenticated symmetric encryption for data.
- Hybrid mode must be designed and reviewed against a defined protocol; concatenating secrets ad hoc is not an approved hybrid construction.

## Standards

- NIST FIPS 203 — ML-KEM
- NIST FIPS 204 — ML-DSA
- NIST FIPS 205 — SLH-DSA
- RFC 5869 — HKDF

## License

Apache-2.0. See `LICENSE`.
