use serde::{Deserialize, Serialize};
use thiserror::Error;

#[derive(Debug, Clone, Copy, Serialize, Deserialize, PartialEq, Eq)]
pub enum Algorithm {
    MlKem768,
    MlDsa65,
    SlhDsa,
    Aes256Gcm,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct OperationPolicy {
    pub algorithm: Algorithm,
    pub purpose: String,
    pub require_audit: bool,
}

#[derive(Debug, Error)]
pub enum PolicyError {
    #[error("operation purpose must not be empty")]
    EmptyPurpose,
    #[error("algorithm is not permitted for this operation")]
    AlgorithmNotPermitted,
}

/// Validates policy metadata only. This crate intentionally does not implement
/// cryptographic primitives; use a maintained and reviewed provider.
pub fn validate_policy(policy: &OperationPolicy) -> Result<(), PolicyError> {
    if policy.purpose.trim().is_empty() {
        return Err(PolicyError::EmptyPurpose);
    }
    Ok(())
}

#[cfg(test)]
mod tests {
    use super::*;
    #[test]
    fn rejects_empty_purpose() {
        let p = OperationPolicy { algorithm: Algorithm::MlKem768, purpose: " ".into(), require_audit: true };
        assert!(matches!(validate_policy(&p), Err(PolicyError::EmptyPurpose)));
    }
}
