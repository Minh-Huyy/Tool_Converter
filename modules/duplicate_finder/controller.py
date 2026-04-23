from .service import DuplicateFinderService

class DuplicateFinderController:
    @classmethod
    def scan_for_duplicates(cls, folder_path: str):
        if not folder_path: return False, "Vui lòng chọn thư mục.", {}
        duplicates = DuplicateFinderService.find_duplicates(folder_path)
        return True, "Scan hoàn tất.", duplicates

    @classmethod
    def delete_duplicates(cls, file_paths: list):
        if not file_paths: return False, "Không có file nào được chọn để xóa.", 0
        count, errors = DuplicateFinderService.delete_files(file_paths)
        if errors:
            return False, f"Đã xóa {count} file, nhưng gặp {len(errors)} lỗi.", count
        return True, f"Đã xóa thành công {count} file trùng lặp.", count
