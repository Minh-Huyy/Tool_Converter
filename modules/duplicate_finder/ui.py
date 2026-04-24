import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from tkinterdnd2 import DND_FILES
from .controller import DuplicateFinderController

class DuplicateFinderUI(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.controller = DuplicateFinderController()
        self.path_var = tk.StringVar()
        self.duplicates_data = {}
        self.setup_ui()

    def setup_ui(self):
        main_frame = tk.Frame(self, padx=20, pady=20)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        tk.Label(main_frame, text="Tìm kiếm File/Thư mục trùng lặp:", font=("Arial", 10, "bold")).pack(anchor=tk.W, pady=(0, 5))
        
        # Path selection
        path_frame = tk.Frame(main_frame)
        path_frame.pack(fill=tk.X, pady=(0, 10))
        tk.Entry(path_frame, textvariable=self.path_var).pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))
        tk.Button(path_frame, text="📁 Chọn...", command=self.browse).pack(side=tk.RIGHT)
        
        # Mode selection
        mode_frame = tk.Frame(main_frame)
        mode_frame.pack(fill=tk.X, pady=(0, 10))
        tk.Label(mode_frame, text="Chế độ quét:", font=("Arial", 10)).pack(side=tk.LEFT, padx=(0, 10))
        self.mode_var = tk.StringVar(value="file")
        tk.Radiobutton(mode_frame, text="Tệp tin", variable=self.mode_var, value="file").pack(side=tk.LEFT, padx=5)
        tk.Radiobutton(mode_frame, text="Thư mục", variable=self.mode_var, value="folder").pack(side=tk.LEFT, padx=5)

        # Buttons
        btn_frame = tk.Frame(main_frame)
        btn_frame.pack(fill=tk.X, pady=5)
        tk.Button(btn_frame, text="🔍 QUÉT TRÙNG LẶP", bg="#FF9800", fg="white", command=self.on_scan, width=20).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="🗑️ XÓA CÁC BẢN SAO", bg="#F44336", fg="white", command=self.on_delete, width=20).pack(side=tk.LEFT, padx=5)
        
        # Treeview for results
        self.tree = ttk.Treeview(main_frame, columns=("Status", "Path", "Info"), show="headings")
        self.tree.heading("Status", text="Trạng thái")
        self.tree.heading("Path", text="Đường dẫn")
        self.tree.heading("Info", text="Thông tin")
        
        self.tree.column("Status", width=120, anchor=tk.CENTER)
        self.tree.column("Path", width=500)
        self.tree.column("Info", width=150, anchor=tk.CENTER)
        
        self.tree.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # Scrollbar
        sb = ttk.Scrollbar(self.tree, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=sb.set)
        sb.pack(side=tk.RIGHT, fill=tk.Y)

        # Drag & Drop
        self.drop_target_register(DND_FILES)
        self.dnd_bind('<<Drop>>', self.on_drop)

    def browse(self):
        p = filedialog.askdirectory()
        if p: self.path_var.set(p)

    def on_drop(self, event):
        path = event.data
        if path.startswith('{') and path.endswith('}'):
            path = path[1:-1]
        self.path_var.set(path)

    def on_scan(self):
        mode = self.mode_var.get()
        s, m, data = self.controller.scan_for_duplicates(self.path_var.get(), mode)
        if not s:
            messagebox.showwarning("Cảnh báo", m)
            return
            
        self.duplicates_data = data
        for i in self.tree.get_children(): self.tree.delete(i)
        
        count = 0
        for sig, paths in data.items():
            # Extract info from signature for display
            info = ""
            if mode == "folder":
                parts = sig.split('|')
                if len(parts) >= 2:
                    file_count = parts[0]
                    total_size = int(parts[1]) / 1024 / 1024
                    info = f"{file_count} files, {total_size:.2f} MB"
            
            for i, p in enumerate(paths):
                if i == 0:
                    status = "⭐ Bản gốc"
                    tag = "original"
                else:
                    status = "❌ Bản sao"
                    tag = "duplicate"
                    count += 1
                
                if mode == "file":
                    info = f"{os.path.getsize(p) / 1024:.1f} KB"
                
                self.tree.insert("", tk.END, values=(status, p, info), tags=(tag,))
        
        self.tree.tag_configure("duplicate", background="#FFF3E0", foreground="#E65100")
        self.tree.tag_configure("original", background="#E8F5E9", foreground="#2E7D32")
        messagebox.showinfo("Xong", f"Tìm thấy {len(data)} nhóm trùng lặp ({count} bản sao).")

    def on_delete(self):
        if not self.duplicates_data:
            messagebox.showwarning("Cảnh báo", "Hãy quét trước!")
            return
            
        mode = self.mode_var.get()
        to_delete = []
        for sig, paths in self.duplicates_data.items():
            to_delete.extend(paths[1:]) # Keep the first one
            
        if not to_delete:
            messagebox.showinfo("Thông báo", "Không có bản sao nào để xóa.")
            return
            
        item_type = "file" if mode == "file" else "thư mục"
        if messagebox.askyesno("Xác nhận", f"Bạn có chắc muốn xóa {len(to_delete)} {item_type} bản sao?"):
            s, m, count = self.controller.delete_duplicates(to_delete, is_folder=(mode == "folder"))
            if s: messagebox.showinfo("Thành công", m)
            else: messagebox.showerror("Lỗi", m)
            self.on_scan() # Rescan
import os
