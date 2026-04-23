import os
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from .controller import DownloaderController

class DownloaderUI(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg="white")
        self.controller = DownloaderController(self)
        self.setup_ui()

    def setup_ui(self):
        # Main container with padding
        container = tk.Frame(self, bg="white", padx=40, pady=40)
        container.pack(fill=tk.BOTH, expand=True)

        # Title
        tk.Label(
            container, 
            text="⬇️ URL Downloader", 
            font=("Arial", 24, "bold"), 
            bg="white", 
            fg="#2C3E50"
        ).pack(anchor="w", pady=(0, 20))

        # Description
        tk.Label(
            container, 
            text="Tải xuống tệp tin từ URL với tốc độ cao và hỗ trợ tệp lớn.", 
            font=("Arial", 11), 
            bg="white", 
            fg="#7F8C8D"
        ).pack(anchor="w", pady=(0, 30))

        # Input Section
        input_card = tk.LabelFrame(container, text=" Cấu hình tải xuống ", font=("Arial", 10, "bold"), bg="white", padx=20, pady=20)
        input_card.pack(fill=tk.X, pady=(0, 20))

        # URL Entry
        tk.Label(input_card, text="Đường dẫn URL:", font=("Arial", 10), bg="white").pack(anchor="w")
        self.url_var = tk.StringVar()
        self.url_entry = tk.Entry(input_card, textvariable=self.url_var, font=("Arial", 12), relief=tk.SOLID, bd=1)
        self.url_entry.pack(fill=tk.X, pady=(5, 15))

        # Save Path
        tk.Label(input_card, text="Lưu tại thư mục:", font=("Arial", 10), bg="white").pack(anchor="w")
        path_frame = tk.Frame(input_card, bg="white")
        path_frame.pack(fill=tk.X, pady=(5, 0))
        
        self.path_var = tk.StringVar(value=os.path.expanduser("~/Downloads"))
        self.path_entry = tk.Entry(path_frame, textvariable=self.path_var, font=("Arial", 10), relief=tk.SOLID, bd=1)
        self.path_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, ipady=3)
        
        btn_browse = tk.Button(
            path_frame, 
            text="Chọn...", 
            command=self.browse_path,
            bg="#34495E", 
            fg="white", 
            relief=tk.FLAT, 
            padx=15
        )
        btn_browse.pack(side=tk.RIGHT, padx=(10, 0))

        # Progress Section
        self.progress_frame = tk.Frame(container, bg="white")
        self.progress_frame.pack(fill=tk.X, pady=20)

        self.progress_bar = ttk.Progressbar(self.progress_frame, orient="horizontal", mode="determinate")
        self.progress_bar.pack(fill=tk.X, pady=(0, 5))

        self.status_label = tk.Label(self.progress_frame, text="Sẵn sàng", font=("Arial", 10), bg="white", fg="#34495E")
        self.status_label.pack(side=tk.LEFT)

        self.stats_label = tk.Label(self.progress_frame, text="", font=("Arial", 10), bg="white", fg="#7F8C8D")
        self.stats_label.pack(side=tk.RIGHT)

        # Download Button
        self.btn_download = tk.Button(
            container, 
            text="🚀 BẮT ĐẦU TẢI XUỐNG", 
            font=("Arial", 12, "bold"),
            bg="#1ABC9C", 
            fg="white", 
            relief=tk.FLAT, 
            pady=12,
            cursor="hand2",
            command=self.start_download
        )
        self.btn_download.pack(fill=tk.X, pady=20)

    def browse_path(self):
        path = filedialog.askdirectory()
        if path:
            self.path_var.set(path)

    def start_download(self):
        url = self.url_var.get().strip()
        save_dir = self.path_var.get().strip()
        self.controller.start_download(url, save_dir)

    def update_progress(self, percent, stats):
        self.progress_bar["value"] = percent
        self.stats_label.config(text=stats)
        self.update_idletasks()

    def update_status(self, status):
        self.status_label.config(text=status)
        if "Success" in status:
            messagebox.showinfo("Thành công", status)

    def show_error(self, message):
        messagebox.showerror("Lỗi", message)

    def set_loading(self, is_loading):
        if is_loading:
            self.btn_download.config(state=tk.DISABLED, text="⌛ ĐANG TẢI...", bg="#95A5A6")
        else:
            self.btn_download.config(state=tk.NORMAL, text="🚀 BẮT ĐẦU TẢI XUỐNG", bg="#1ABC9C")

