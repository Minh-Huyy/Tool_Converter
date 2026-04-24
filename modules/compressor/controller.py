import threading
import os
from .service import CompressorService

class CompressorController:
    def __init__(self, ui):
        self.ui = ui
        self.service = CompressorService()

    def check_rar_support(self):
        return self.service.is_rar_supported()

    def start_compression(self, source_paths: list[str], format: str, output_dir: str):
        if not source_paths:
            self.ui.show_error("Vui lòng chọn ít nhất một file hoặc thư mục!")
            return
        
        # Check if all paths exist
        for path in source_paths:
            if not os.path.exists(path):
                self.ui.show_error(f"Đường dẫn không tồn tại: {path}")
                return

        if not output_dir:
            self.ui.show_error("Vui lòng chọn thư mục lưu!")
            return

        self.ui.set_loading(True)
        
        # Run in separate thread to keep UI responsive
        thread = threading.Thread(
            target=self.service.compress,
            args=(
                source_paths,
                format,
                output_dir,
                self.update_status,
                self.handle_error
            ),
            daemon=True
        )
        thread.start()

    def update_status(self, status: str):
        self.ui.update_status(status)
        if "Thành công" in status:
            self.ui.set_loading(False)

    def handle_error(self, error_msg: str):
        self.ui.show_error(error_msg)
        self.ui.set_loading(False)
