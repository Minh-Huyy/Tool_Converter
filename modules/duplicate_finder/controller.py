import os
from .service import DuplicateFinderService

class DuplicateFinderController:
    def __init__(self):
        self.service = DuplicateFinderService()

    def scan_for_duplicates(self, path: str, mode: str = "file") -> tuple[bool, str, dict]:
        if not path or not os.path.exists(path):
            return False, "Đường dẫn không hợp lệ!", {}
            
        try:
            if mode == "folder":
                data = self.service.find_duplicate_folders(path)
            else:
                data = self.service.find_duplicates(path)
            return True, "Thành công", data
        except Exception as e:
            return False, f"Lỗi: {str(e)}", {}

    def delete_duplicates(self, paths: list, is_folder: bool = False) -> tuple[bool, str, int]:
        count, errors = self.service.delete_items(paths, is_folder)
        if errors:
            return False, f"Đã xóa {count} mục. Lỗi: {'; '.join(errors)}", count
        return True, f"Đã xóa thành công {count} mục.", count
