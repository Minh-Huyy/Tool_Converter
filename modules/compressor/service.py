import os
import zipfile
import subprocess
from typing import Callable, Optional

class CompressorService:
    def __init__(self):
        self.winrar_path = self._detect_winrar()

    def _detect_winrar(self) -> Optional[str]:
        """Detect WinRAR installation path."""
        common_paths = [
            r"C:\Program Files\WinRAR\rar.exe",
            r"C:\Program Files (x86)\WinRAR\rar.exe",
            r"C:\Program Files\WinRAR\WinRAR.exe",
        ]
        
        # Check PATH first
        try:
            subprocess.run(["rar", "/?"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            return "rar"
        except FileNotFoundError:
            pass

        for path in common_paths:
            if os.path.exists(path):
                return path
        return None

    def is_rar_supported(self) -> bool:
        return self.winrar_path is not None

    def compress(
        self, 
        source_paths: list[str], 
        format: str, 
        output_dir: str,
        progress_callback: Callable[[str], None],
        error_callback: Callable[[str], None]
    ):
        """Main compression method."""
        try:
            if not source_paths:
                error_callback("Chưa chọn file/thư mục để nén!")
                return False

            # Use the name of the first item as the base for the archive name
            base_name = os.path.basename(source_paths[0].rstrip(os.sep))
            if len(source_paths) > 1:
                base_name += f"_and_{len(source_paths)-1}_others"

            if format.lower() == "zip":
                output_path = os.path.join(output_dir, f"{base_name}.zip")
                return self._compress_zip(source_paths, output_path, progress_callback)
            elif format.lower() == "rar":
                if not self.winrar_path:
                    error_callback("Không tìm thấy WinRAR trên hệ thống!")
                    return False
                output_path = os.path.join(output_dir, f"{base_name}.rar")
                return self._compress_rar(source_paths, output_path, progress_callback)
            else:
                error_callback(f"Định dạng {format} không được hỗ trợ!")
                return False

        except Exception as e:
            error_callback(f"Lỗi nén: {str(e)}")
            return False

    def _compress_zip(self, source_paths: list[str], output_path: str, progress_callback: Callable[[str], None]):
        """Compress multiple items using standard zipfile module."""
        progress_callback("Đang nén ZIP...")
        with zipfile.ZipFile(output_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for sp in source_paths:
                if not os.path.exists(sp): continue
                if os.path.isdir(sp):
                    base_dir = os.path.dirname(sp)
                    for root, dirs, files in os.walk(sp):
                        for file in files:
                            file_path = os.path.join(root, file)
                            arcname = os.path.relpath(file_path, base_dir)
                            zipf.write(file_path, arcname)
                else:
                    zipf.write(sp, os.path.basename(sp))
        progress_callback(f"Thành công! Đã lưu tại {os.path.basename(output_path)}")
        return True

    def _compress_rar(self, source_paths: list[str], output_path: str, progress_callback: Callable[[str], None]):
        """Compress multiple items using WinRAR CLI."""
        progress_callback("Đang nén RAR (Sử dụng WinRAR)...")
        
        # Commands: a (add), -r (recursive), -ep1 (exclude base directory from path)
        # For multiple paths, we just add them all to the command line
        cmd = [self.winrar_path, "a", "-r", "-ep1", output_path] + source_paths
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode == 0:
            progress_callback(f"Thành công! Đã lưu tại {os.path.basename(output_path)}")
            return True
        else:
            raise Exception(f"WinRAR Error: {result.stderr or result.stdout}")
