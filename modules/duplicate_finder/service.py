import os
import hashlib

class DuplicateFinderService:
    @staticmethod
    def get_file_hash(file_path: str, block_size=65536) -> str:
        hasher = hashlib.md5()
        try:
            with open(file_path, 'rb') as f:
                for block in iter(lambda: f.read(block_size), b''):
                    hasher.update(block)
            return hasher.hexdigest()
        except Exception:
            return ""

    @classmethod
    def find_duplicates(cls, folder_path: str) -> dict:
        hashes = {}
        duplicates = {}
        
        for root, _, files in os.walk(folder_path):
            for filename in files:
                full_path = os.path.join(root, filename)
                file_hash = cls.get_file_hash(full_path)
                
                if file_hash:
                    if file_hash not in hashes:
                        hashes[file_hash] = []
                    hashes[file_hash].append(full_path)
        
        # Lọc ra các nhóm có nhiều hơn 1 file và sắp xếp để chọn "Bản gốc" thông minh hơn
        final_duplicates = {}
        for hash_val, paths in hashes.items():
            if len(paths) > 1:
                # Sắp xếp: Ưu tiên đường dẫn ngắn nhất (thường là file gốc), 
                # sau đó đến thời gian tạo cũ nhất
                paths.sort(key=lambda p: (len(p), os.path.getctime(p)))
                final_duplicates[hash_val] = paths
        
        return final_duplicates

    @staticmethod
    def delete_files(file_paths: list) -> tuple[int, list]:
        deleted_count = 0
        errors = []
        for path in file_paths:
            try:
                if os.path.exists(path):
                    os.remove(path)
                    deleted_count += 1
            except Exception as e:
                errors.append(f"Lỗi khi xóa {path}: {e}")
        return deleted_count, errors
