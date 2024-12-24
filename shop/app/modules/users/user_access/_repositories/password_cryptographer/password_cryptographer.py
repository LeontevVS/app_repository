import hashlib
import os

from .proto import PasswordCryptographerP


class PasswordCryptographer(PasswordCryptographerP):
    async def encrypt_password(
        self,
        password: bytes,
        salt: bytes,
        iterations: int = 100_000,
        hash_name: str = "sha256",
    ) -> bytes:
        return hashlib.pbkdf2_hmac(
            hash_name=hash_name,
            password=password,
            salt=salt,
            iterations=iterations,
        )

    async def generate_salt(self, salt_length: int = 16) -> bytes:
        return os.urandom(salt_length)


def get_password_cryptographer() -> PasswordCryptographerP:
    return PasswordCryptographer()
