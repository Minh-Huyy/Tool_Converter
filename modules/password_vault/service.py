import json
import os
import base64
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

class PasswordVaultService:
    def __init__(self, data_dir="data"):
        self.data_dir = data_dir
        self.file_path = os.path.join(self.data_dir, "vault.bin")
        self.salt_path = os.path.join(self.data_dir, "salt.bin")
        self.fernet = None
        
        if not os.path.exists(self.data_dir):
            os.makedirs(self.data_dir)

    def _derive_key(self, password, salt):
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
        )
        return base64.urlsafe_b64encode(kdf.derive(password.encode()))

    def initialize_vault(self, master_password):
        """Tạo vault mới lần đầu"""
        salt = os.urandom(16)
        with open(self.salt_path, "wb") as f:
            f.write(salt)
        
        key = self._derive_key(master_password, salt)
        self.fernet = Fernet(key)
        self._save_data([])
        return True

    def unlock(self, master_password):
        """Mở khóa vault với mật khẩu chủ"""
        if not os.path.exists(self.salt_path):
            return False
            
        with open(self.salt_path, "rb") as f:
            salt = f.read()
            
        key = self._derive_key(master_password, salt)
        self.fernet = Fernet(key)
        
        try:
            self._load_data()
            return True
        except Exception:
            self.fernet = None
            return False

    def is_initialized(self):
        return os.path.exists(self.file_path) and os.path.exists(self.salt_path)

    def _save_data(self, data):
        json_data = json.dumps(data).encode()
        encrypted_data = self.fernet.encrypt(json_data)
        with open(self.file_path, "wb") as f:
            f.write(encrypted_data)

    def _load_data(self):
        if not os.path.exists(self.file_path):
            return []
        with open(self.file_path, "rb") as f:
            encrypted_data = f.read()
        decrypted_data = self.fernet.decrypt(encrypted_data)
        return json.loads(decrypted_data.decode())

    def get_all_accounts(self):
        return self._load_data()

    def add_account(self, account_data):
        data = self._load_data()
        # Thêm ID duy nhất
        account_data["id"] = os.urandom(8).hex()
        data.append(account_data)
        self._save_data(data)
        return account_data

    def update_account(self, account_id, updated_data):
        data = self._load_data()
        for i, acc in enumerate(data):
            if acc["id"] == account_id:
                updated_data["id"] = account_id
                data[i] = updated_data
                self._save_data(data)
                return True
        return False

    def delete_account(self, account_id):
        data = self._load_data()
        new_data = [acc for acc in data if acc["id"] != account_id]
        if len(new_data) < len(data):
            self._save_data(new_data)
            return True
        return False
