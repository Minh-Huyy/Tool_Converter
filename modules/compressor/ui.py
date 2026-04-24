import os
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from tkinterdnd2 import DND_FILES
from .controller import CompressorController

class CompressorUI(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg="white")
        self.controller = CompressorController(self)
        self.source_paths = []
        self.setup_ui()
        self.check_rar_status()

    def setup_ui(self):
        # Main container with padding
        container = tk.Frame(self, bg="white", padx=40, pady=40)
        container.pack(fill=tk.BOTH, expand=True)

        # Title
        tk.Label(
            container, 
            text="📦 Folder Compressor", 
            font=("Arial", 24, "bold"), 
            bg="white", 
            fg="#2C3E50"
        ).pack(anchor="w", pady=(0, 10))

        # Description
        tk.Label(
            container, 
            text="Nén nhiều tệp và thư mục thành định dạng ZIP hoặc RAR.", 
            font=("Arial", 11), 
            bg="white", 
            fg="#7F8C8D"
        ).pack(anchor="w", pady=(0, 30))

        # Input Section
        input_card = tk.LabelFrame(container, text=" Cấu hình nén ", font=("Arial", 10, "bold"), bg="white", padx=20, pady=20)
        input_card.pack(fill=tk.X, pady=(0, 20))

        # Source Paths (Listbox)
        tk.Label(input_card, text="Danh sách tệp/thư mục cần nén:", font=("Arial", 10), bg="white").pack(anchor="w")
        
        list_frame = tk.Frame(input_card, bg="white")
        list_frame.pack(fill=tk.X, pady=(5, 10))
        
        self.src_listbox = tk.Listbox(list_frame, height=5, font=("Arial", 9), relief=tk.SOLID, bd=1)
        self.src_listbox.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        sb = tk.Scrollbar(list_frame, orient="vertical", command=self.src_listbox.yview)
        sb.pack(side=tk.RIGHT, fill=tk.Y)
        self.src_listbox.config(yscrollcommand=sb.set)
        
        btn_src_frame = tk.Frame(input_card, bg="white")
        btn_src_frame.pack(fill=tk.X, pady=(0, 15))
        
        tk.Button(btn_src_frame, text="📁 Thêm thư mục...", command=self.browse_src_dir, bg="#34495E", fg="white", padx=10).pack(side=tk.LEFT, padx=(0, 10))
        tk.Button(btn_src_frame, text="📄 Thêm tệp...", command=self.browse_src_file, bg="#34495E", fg="white", padx=10).pack(side=tk.LEFT, padx=(0, 10))
        tk.Button(btn_src_frame, text="❌ Xóa hết", command=self.clear_list, bg="#95A5A6", fg="white", padx=10).pack(side=tk.LEFT)

        # Format Selection
        tk.Label(input_card, text="Định dạng nén:", font=("Arial", 10), bg="white").pack(anchor="w")
        format_frame = tk.Frame(input_card, bg="white")
        format_frame.pack(fill=tk.X, pady=(5, 15))
        
        self.format_var = tk.StringVar(value="zip")
        self.rb_zip = tk.Radiobutton(format_frame, text="ZIP (.zip)", variable=self.format_var, value="zip", bg="white", font=("Arial", 10))
        self.rb_zip.pack(side=tk.LEFT, padx=(0, 20))
        
        self.rb_rar = tk.Radiobutton(format_frame, text="RAR (.rar)", variable=self.format_var, value="rar", bg="white", font=("Arial", 10))
        self.rb_rar.pack(side=tk.LEFT)
        
        self.rar_status_label = tk.Label(format_frame, text="", font=("Arial", 9, "italic"), bg="white")
        self.rar_status_label.pack(side=tk.LEFT, padx=10)

        # Save Path
        tk.Label(input_card, text="Lưu tại thư mục:", font=("Arial", 10), bg="white").pack(anchor="w")
        dest_frame = tk.Frame(input_card, bg="white")
        dest_frame.pack(fill=tk.X, pady=(5, 0))
        
        self.dest_var = tk.StringVar(value=os.path.expanduser("~/Desktop"))
        self.dest_entry = tk.Entry(dest_frame, textvariable=self.dest_var, font=("Arial", 10), relief=tk.SOLID, bd=1)
        self.dest_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, ipady=3)
        
        btn_browse_dest = tk.Button(
            dest_frame, 
            text="Chọn...", 
            command=self.browse_dest,
            bg="#34495E", 
            fg="white", 
            relief=tk.FLAT, 
            padx=15
        )
        btn_browse_dest.pack(side=tk.RIGHT, padx=(10, 0))

        # Progress Section
        self.progress_frame = tk.Frame(container, bg="white")
        self.progress_frame.pack(fill=tk.X, pady=20)

        self.status_label = tk.Label(self.progress_frame, text="Sẵn sàng", font=("Arial", 10), bg="white", fg="#34495E")
        self.status_label.pack(side=tk.LEFT)

        # Compress Button
        self.btn_compress = tk.Button(
            container, 
            text="📦 BẮT ĐẦU NÉN", 
            font=("Arial", 12, "bold"),
            bg="#3498DB", 
            fg="white", 
            relief=tk.FLAT, 
            pady=12,
            cursor="hand2",
            command=self.start_compression
        )
        self.btn_compress.pack(fill=tk.X, pady=20)

        # Drag & Drop
        self.drop_target_register(DND_FILES)
        self.dnd_bind('<<Drop>>', self.on_drop)

    def check_rar_status(self):
        if not self.controller.check_rar_support():
            self.rb_rar.config(state=tk.DISABLED)
            self.rar_status_label.config(text="(WinRAR chưa được cài đặt - Chỉ hỗ trợ ZIP)", fg="#E74C3C")
            self.format_var.set("zip")
        else:
            self.rar_status_label.config(text="(Đã phát hiện WinRAR)", fg="#27AE60")

    def browse_src_dir(self):
        path = filedialog.askdirectory()
        if path: self.add_to_list(path)

    def browse_src_file(self):
        paths = filedialog.askopenfilenames()
        if paths:
            for p in paths: self.add_to_list(p)

    def add_to_list(self, path):
        if path not in self.source_paths:
            self.source_paths.append(path)
            self.src_listbox.insert(tk.END, os.path.basename(path))
            # Auto set destination
            if len(self.source_paths) == 1:
                self.dest_var.set(os.path.dirname(path))

    def clear_list(self):
        self.source_paths = []
        self.src_listbox.delete(0, tk.END)

    def browse_dest(self):
        path = filedialog.askdirectory()
        if path:
            self.dest_var.set(path)

    def on_drop(self, event):
        data = event.data
        import re
        paths = re.findall(r'\{.*?\}|\S+', data)
        paths = [p[1:-1] if p.startswith('{') and p.endswith('}') else p for p in paths]
        for p in paths:
            self.add_to_list(p)

    def start_compression(self):
        fmt = self.format_var.get()
        dest = self.dest_var.get().strip()
        self.controller.start_compression(self.source_paths, fmt, dest)

    def update_status(self, status):
        self.status_label.config(text=status)
        if "Thành công" in status:
            messagebox.showinfo("Thành công", status)

    def show_error(self, message):
        messagebox.showerror("Lỗi", message)

    def set_loading(self, is_loading):
        if is_loading:
            self.btn_compress.config(state=tk.DISABLED, text="⌛ ĐANG NÉN...", bg="#95A5A6")
        else:
            self.btn_compress.config(state=tk.NORMAL, text="📦 BẮT ĐẦU NÉN", bg="#3498DB")

