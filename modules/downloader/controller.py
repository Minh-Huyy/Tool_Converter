import threading
from .service import DownloaderService

class DownloaderController:
    def __init__(self, ui):
        self.ui = ui
        self.service = DownloaderService()

    def start_download(self, url: str, save_dir: str):
        if not url:
            self.ui.show_error("Vui lòng nhập URL!")
            return
        
        if not save_dir:
            self.ui.show_error("Vui lòng chọn thư mục lưu!")
            return

        # Start download in a separate thread
        thread = threading.Thread(
            target=self.service.download_file,
            args=(
                url,
                save_dir,
                self.update_progress,
                self.update_status,
                self.handle_error
            ),
            daemon=True
        )
        thread.start()
        self.ui.set_loading(True)

    def update_progress(self, downloaded, total, speed):
        if total > 0:
            percent = (downloaded / total) * 100
            self.ui.update_progress(percent, f"{downloaded / 1024 / 1024:.2f} MB / {total / 1024 / 1024:.2f} MB")
        else:
            self.ui.update_progress(0, f"{downloaded / 1024 / 1024:.2f} MB (Unknown size)")

    def update_status(self, status: str):
        self.ui.update_status(status)
        if "Success" in status:
            self.ui.set_loading(False)

    def handle_error(self, error_msg: str):
        self.ui.show_error(error_msg)
        self.ui.set_loading(False)
