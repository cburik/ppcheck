import base64
import getpass
import os
from functools import lru_cache

from cryptography.fernet import Fernet, InvalidToken
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

from ppcheck.settings import get_settings


class EncryptionManager:
    _instance = None
    _password = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    @staticmethod
    def generate_salt() -> bytes:
        return os.urandom(16)

    def encrypt(self, data: bytes, salt: bytes) -> bytes:
        if self._password is None:
            self._get_password()
        fernet = self._initialize_fernet(salt)
        return fernet.encrypt(data)

    def encrypt_str(self, data: str, salt: bytes) -> bytes:
        return self.encrypt(data.encode(), salt)

    def decrypt(self, data: bytes, salt: bytes) -> bytes:
        if self._password is None:
            self._get_password()
        try:
            fernet = self._initialize_fernet(salt)
            return fernet.decrypt(data)
        except InvalidToken:
            raise ValueError("Invalid token")

    def decrypt_str(self, data: bytes, salt: bytes) -> str:
        return self.decrypt(data, salt).decode()

    def _get_password(self) -> None:
        settings = get_settings()
        if settings.master_password:
            self._password = settings.master_password.encode()
        else:
            self._password = getpass.getpass("Enter encryption password: ").encode()

    @lru_cache(maxsize=1024)
    def _initialize_fernet(self, salt):
        settings = get_settings()
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=settings.pbkdf2_iterations,
        )
        key = base64.urlsafe_b64encode(kdf.derive(self._password))
        return Fernet(key)
