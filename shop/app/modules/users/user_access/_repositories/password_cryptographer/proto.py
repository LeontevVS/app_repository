from typing import Protocol


class PasswordCryptographerP(Protocol):
    async def encrypt_password(self, password: bytes, salt: bytes, iterations: int = 0, hash_name: str = "") -> bytes:
        pass

    async def generate_salt(self, salt_length: int = 0) -> bytes:
        pass
