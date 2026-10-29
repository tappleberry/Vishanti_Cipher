import os

from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives.kdf.argon2 import Argon2id


MAGIC = b"check"


def derive_key(password, salt):
    kdf = Argon2id(
        salt=salt,
        length=32,
        iterations=3,
        lanes=4,
        memory_cost=65536
    )

    return kdf.derive(password.encode())


def encrypt_message(message, password):
    salt = os.urandom(16)
    nonce = os.urandom(12)

    key = derive_key(password, salt)

    aes = AESGCM(key)
    ciphertext = aes.encrypt(
        nonce,
        message.encode(),
        MAGIC
    )

    return MAGIC + salt + nonce + ciphertext


def decrypt_message(payload, password):
    # Verify the payload header
    if not payload.startswith(MAGIC):
        raise ValueError("Invalid payload header. The extracted data may be corrupted.")

    # MAGIC is 5 bytes long
    offset = len(MAGIC)

    # Check minimum payload length:
    # 5-byte header + 16-byte salt + 12-byte nonce + 16-byte GCM tag
    minimum_length = offset + 16 + 12 + 16

    if len(payload) < minimum_length:
        raise ValueError("Payload is too short or corrupted.")

    # Extract the components
    salt = payload[offset:offset + 16]
    nonce = payload[offset + 16:offset + 28]
    ciphertext = payload[offset + 28:]

    # Derive the key
    key = derive_key(password, salt)

    # Decrypt and authenticate
    aes = AESGCM(key)

    plaintext = aes.decrypt(
        nonce,
        ciphertext,
        MAGIC
    )

    return plaintext.decode("utf-8")