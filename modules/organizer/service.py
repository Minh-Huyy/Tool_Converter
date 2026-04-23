import os
import shutil

class FileOrganizerService:
    CATEGORIES = {
        "Images": [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".webp", ".tiff", ".svg", ".ico"],
        "Documents": [".pdf", ".docx", ".doc", ".txt", ".xlsx", ".xls", ".pptx", ".ppt", ".csv", ".rtf"],
        "Videos": [".mp4", ".mkv", ".avi", ".mov", ".wmv", ".flv", ".webm", ".m4v"],
        "Audio": [".mp3", ".wav", ".ogg", ".flac", ".aac", ".m4a", ".wma"],
        "Archives": [".zip", ".rar", ".7z", ".tar", ".gz", ".bz2"],
        "Executables": [".exe", ".msi", ".bat", ".sh"]
    }

    @classmethod
    def organize_folder(cls, folder_path: str) -> tuple[bool, str, list[str]]:
        if not os.path.isdir(folder_path):
            return False, "Đường dẫn không phải thư mục.", []
        
        logs = []
        files_moved = 0
        try:
            for filename in os.listdir(folder_path):
                file_path = os.path.join(folder_path, filename)
                if os.path.isfile(file_path):
                    _, ext = os.path.splitext(filename)
                    ext = ext.lower()
                    target_category = "Others"
                    for category, extensions in cls.CATEGORIES.items():
                        if ext in extensions:
                            target_category = category
                            break
                    
                    target_dir = os.path.join(folder_path, target_category)
                    if not os.path.exists(target_dir): os.makedirs(target_dir)
                    
                    dest_path = os.path.join(target_dir, filename)
                    if os.path.exists(dest_path):
                        name, e = os.path.splitext(filename)
                        c = 1
                        while os.path.exists(os.path.join(target_dir, f"{name}_{c}{e}")): c += 1
                        dest_path = os.path.join(target_dir, f"{name}_{c}{e}")
                        filename = f"{name}_{c}{e}"

                    shutil.move(file_path, dest_path)
                    logs.append(f"Moved: {filename} -> {target_category}/")
                    files_moved += 1
            return True, f"Sắp xếp xong {files_moved} tệp! ✅", logs
        except Exception as e:
            return False, f"Lỗi: {e}", logs
