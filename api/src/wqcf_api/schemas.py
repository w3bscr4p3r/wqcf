from pydantic import BaseModel, Field
from typing import Literal

class KEMGenerateResponse(BaseModel):
    algorithm: str
    public_key: str
    key_id: str
    note: str

class KEMEncapsulateRequest(BaseModel):
    algorithm: Literal["ML-KEM-768"] = "ML-KEM-768"
    public_key: str = Field(min_length=1)

class KEMEncapsulateResponse(BaseModel):
    algorithm: str
    ciphertext: str
    shared_secret: str
    warning: str

class EncryptRequest(BaseModel):
    plaintext_b64: str
    key_b64: str
    associated_data_b64: str = ""

class EncryptResponse(BaseModel):
    algorithm: str
    nonce_b64: str
    ciphertext_b64: str

class SignRequest(BaseModel):
    algorithm: Literal["ML-DSA-65"] = "ML-DSA-65"
    message_b64: str

class VerifyRequest(BaseModel):
    algorithm: Literal["ML-DSA-65"] = "ML-DSA-65"
    message_b64: str
    signature_b64: str
    public_key_b64: str
