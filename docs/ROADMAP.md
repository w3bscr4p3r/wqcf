# Roadmap

## 0.1 — Foundation scaffold
- [x] Repository structure, OpenAPI-capable API, SDK starting points.
- [x] Rust shared policy/type crate.
- [x] Fail-closed provider loading and capability discovery.
- [ ] CI, SBOM and dependency scanning.

## 0.2 — Cryptographic provider
- [ ] Pin and qualify a maintained liboqs release/provider.
- [ ] Rust provider adapter and Python/Rust FFI boundary.
- [ ] KEM round-trip tests and ML-DSA sign/verify tests.
- [ ] Cross-language test vectors.

## 0.3 — Key custody
- [ ] KMS/HSM abstraction and key references.
- [ ] Non-exportable private keys.
- [ ] Rotation, revocation and tenant-scoped authorization.

## 0.4 — Data envelope
- [ ] Versioned envelope format with algorithm identifiers and key IDs.
- [ ] HKDF context separation and AES-GCM authenticated decryption.
- [ ] Replay protection and canonical serialization.

## 0.5 — Hybrid migration
- [ ] Threat-modeled hybrid key establishment.
- [ ] Downgrade resistance and protocol negotiation.
- [ ] Interoperability and performance benchmarks.

## 1.0 — Production readiness gate
- [ ] Independent cryptographic design review.
- [ ] Security assessment, fuzzing, side-channel review.
- [ ] Operational runbooks, disaster recovery and key compromise procedures.
- [ ] Compliance mapping and documented validation scope.
