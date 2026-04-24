import os
import hashlib
import shutil

class DuplicateFinderService:
    def __init__(self):
        self.file_hash_cache = {}

    def get_file_hash(self, file_path: str, block_size=65536) -> str:
        if file_path in self.file_hash_cache:
            return self.file_hash_cache[file_path]
        
        hasher = hashlib.md5()
        try:
            with open(file_path, 'rb') as f:
                for block in iter(lambda: f.read(block_size), b''):
                    hasher.update(block)
            h = hasher.hexdigest()
            self.file_hash_cache[file_path] = h
            return h
        except Exception:
            return ""

    def find_duplicates(self, folder_path: str) -> dict:
        """Find duplicate files."""
        hashes = {}
        self.file_hash_cache = {} # Clear cache for new scan
        
        for root, _, files in os.walk(folder_path):
            for filename in files:
                full_path = os.path.join(root, filename)
                file_hash = self.get_file_hash(full_path)
                
                if file_hash:
                    if file_hash not in hashes:
                        hashes[file_hash] = []
                    hashes[file_hash].append(full_path)
        
        final_duplicates = {}
        for hash_val, paths in hashes.items():
            if len(paths) > 1:
                paths.sort(key=lambda p: (len(p), os.path.getctime(p)))
                final_duplicates[hash_val] = paths
        
        return final_duplicates

    def find_duplicate_folders(self, root_path: str) -> dict:
        """Find duplicate directories based on content."""
        self.file_hash_cache = {}
        dir_signatures = {} # {signature: [list_of_dir_paths]}
        
        # We need to collect info for every directory
        all_dirs = []
        for root, dirs, _ in os.walk(root_path):
            for d in dirs:
                all_dirs.append(os.path.join(root, d))
        
        for dir_path in all_dirs:
            signature = self._get_directory_signature(dir_path)
            if signature:
                if signature not in dir_signatures:
                    dir_signatures[signature] = []
                dir_signatures[signature].append(dir_path)
        
        # Filter duplicates
        final_duplicates = {}
        for sig, paths in dir_signatures.items():
            if len(paths) > 1:
                # Sort: shortest path first, then oldest
                paths.sort(key=lambda p: (len(p), os.path.getctime(p)))
                final_duplicates[sig] = paths
        
        return final_duplicates

    def _get_directory_signature(self, dir_path: str) -> str:
        """Generate a signature for a directory based on its contents."""
        file_list = []
        total_size = 0
        file_count = 0
        empty_dirs_count = 0
        
        try:
            for root, dirs, files in os.walk(dir_path):
                # Count empty subdirectories to distinguish between folders with different structures
                for d in dirs:
                    d_path = os.path.join(root, d)
                    if not os.listdir(d_path):
                        empty_dirs_count += 1

                for f in files:
                    abs_path = os.path.join(root, f)
                    rel_path = os.path.relpath(abs_path, dir_path)
                    f_hash = self.get_file_hash(abs_path)
                    if f_hash:
                        f_size = os.path.getsize(abs_path)
                        file_list.append((rel_path, f_hash, f_size))
                        total_size += f_size
                        file_count += 1
            
            # If no files and no empty subdirs, it's just an empty folder
            if not file_list and empty_dirs_count == 0:
                return "0|0|empty_folder_content"
                
            # Sort by relative path to ensure consistency
            file_list.sort()
            
            # Create a string representation and hash it
            # Include empty_dirs_count in the signature to differentiate folders with empty subdirs
            content_str = (str(file_list) + f"|empty_dirs:{empty_dirs_count}").encode('utf-8')
            content_hash = hashlib.md5(content_str).hexdigest()
            
            return f"{file_count}|{total_size}|{content_hash}"
        except Exception:
            return ""

    @staticmethod
    def delete_items(paths: list, is_folder: bool = False) -> tuple[int, list]:
        deleted_count = 0
        errors = []
        for path in paths:
            try:
                if os.path.exists(path):
                    if is_folder:
                        shutil.rmtree(path)
                    else:
                        os.remove(path)
                    deleted_count += 1
            except Exception as e:
                errors.append(f"Lỗi khi xóa {path}: {e}")
        return deleted_count, errors
