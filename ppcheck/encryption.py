import base64
import getpass
import os
from abc import ABC, abstractmethod
from functools import lru_cache

from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

from ppcheck.settings import get_settings


class EncryptionBase(ABC):
    _password = None
    _iterations = None

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
        fernet = self._initialize_fernet(salt)
        return fernet.decrypt(data)

    def decrypt_str(self, data: bytes, salt: bytes) -> str:
        return self.decrypt(data, salt).decode()

    @lru_cache(maxsize=1024)
    def _initialize_fernet(self, salt):
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=self._iterations,
        )
        key = base64.urlsafe_b64encode(kdf.derive(self._password))
        return Fernet(key)

    @abstractmethod
    def _get_password(self):
        pass


class EncryptionManager(EncryptionBase):
    _instance = None
    _password = None
    _iterations = get_settings().field_iterations

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def _get_password(self):
        # MasterPassword has to be initialized before encryption manager can be used
        self._password = MasterPasswordManager().get_password()
        return self._password


class MasterPasswordManager(EncryptionBase):
    _instance = None
    _password = None
    _iterations = get_settings().master_iterations

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def _get_master_salt(self) -> bytes:
        settings = get_settings()
        if not settings.master_salt_loc.exists():
            salt = self.generate_salt()
            settings.master_salt_loc.write_bytes(salt)
            return salt
        return settings.master_salt_loc.read_bytes()

    def get_password(self) -> bytes:
        return self._get_password()

    def _get_password(self) -> bytes:
        if self._password is None:
            settings = get_settings()
            if settings.master_password:
                self._password = settings.master_password.encode()
            else:
                try:
                    self._get_password_from_user(tries=3)
                except ValueError as exc:
                    raise ValueError("Failed to get master password after 3 tries") from exc
        return self._password

    def _get_password_from_user(self, tries) -> bytes:
        self._password = getpass.getpass("Enter master password: ").encode()
        if not self._verify_master_password():
            if tries > 1:
                print("Incorrect master password, please try again.")
                return self._get_password_from_user(tries - 1)
            else:
                raise ValueError("Incorrect master password")

    def _verify_master_password(self) -> bool:
        settings = get_settings()
        if not settings.magic_file.exists():
            # First time setup
            magic_data = self.encrypt_str(settings.magic_string, self._get_master_salt())
            settings.magic_file.write_bytes(magic_data)
            return True
        else:
            magic_data = settings.magic_file.read_bytes()
            try:
                decrypted_magic = self.decrypt_str(magic_data, self._get_master_salt())
                return decrypted_magic == settings.magic_string
            except ValueError:
                return False
