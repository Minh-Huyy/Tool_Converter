import random
import string
import pyperclip
from .service import PasswordVaultService

class PasswordVaultController:
    def __init__(self):
        self.service = PasswordVaultService()

    def generate_strong_password(self, length=16):
        characters = string.ascii_letters + string.digits + "!@#$%^&*()"
        return ''.join(random.choice(characters) for _ in range(length))

    def copy_to_clipboard(self, text):
        pyperclip.copy(text)

    def is_vault_ready(self):
        return self.service.is_initialized()

    def setup_vault(self, master_password):
        return self.service.initialize_vault(master_password)

    def unlock_vault(self, master_password):
        return self.service.unlock(master_password)

    def get_accounts(self, search_query=""):
        accounts = self.service.get_all_accounts()
        if not search_query:
            return accounts
        
        query = search_query.lower()
        return [
            acc for acc in accounts 
            if query in acc.get("site", "").lower() or query in acc.get("username", "").lower()
        ]

    def add_account(self, site, username, password, notes=""):
        if not site or not username or not password:
            return False, "Vui lòng điền đầy đủ thông tin bắt buộc."
        
        account_data = {
            "site": site,
            "username": username,
            "password": password,
            "notes": notes
        }
        self.service.add_account(account_data)
        return True, "Đã thêm tài khoản thành công."

    def update_account(self, account_id, site, username, password, notes=""):
        if not site or not username or not password:
            return False, "Vui lòng điền đầy đủ thông tin bắt buộc."
            
        updated_data = {
            "site": site,
            "username": username,
            "password": password,
            "notes": notes
        }
        if self.service.update_account(account_id, updated_data):
            return True, "Đã cập nhật tài khoản."
        return False, "Không tìm thấy tài khoản để cập nhật."

    def delete_account(self, account_id):
        if self.service.delete_account(account_id):
            return True, "Đã xóa tài khoản."
        return False, "Không thể xóa tài khoản."
