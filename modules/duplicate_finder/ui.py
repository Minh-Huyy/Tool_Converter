import tkinter as tk
from tkinter import filedialog, messagebox, ttk
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
        
        tk.Label(main_frame, text="Tìm kiếm File trùng lặp:", font=("Arial", 10, "bold")).pack(anchor=tk.W, pady=(0, 5))
        
        path_frame = tk.Frame(main_frame)
        path_frame.pack(fill=tk.X, pady=(0, 10))
        tk.Entry(path_frame, textvariable=self.path_var).pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))
        tk.Button(path_frame, text="📁 Chọn...", command=self.browse).pack(side=tk.RIGHT)
        
        btn_frame = tk.Frame(main_frame)
        btn_frame.pack(fill=tk.X, pady=5)
        tk.Button(btn_frame, text="🔍 QUÉT FILE TRÙNG", bg="#FF9800", fg="white", command=self.on_scan, width=20).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="🗑️ XÓA CÁC BẢN SAO", bg="#F44336", fg="white", command=self.on_delete, width=20).pack(side=tk.LEFT, padx=5)
        
        # Treeview for results
        self.tree = ttk.Treeview(main_frame, columns=("Status", "Path", "Size"), show="headings")
        self.tree.heading("Status", text="Trạng thái")
        self.tree.heading("Path", text="Đường dẫn File")
        self.tree.heading("Size", text="Kích thước")
        
        self.tree.column("Status", width=120, anchor=tk.CENTER)
        self.tree.column("Path", width=500)
        self.tree.column("Size", width=100, anchor=tk.CENTER)
        
        self.tree.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # Scrollbar
        sb = ttk.Scrollbar(self.tree, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=sb.set)
        sb.pack(side=tk.RIGHT, fill=tk.Y)

    def browse(self):
        p = filedialog.askdirectory()
        if p: self.path_var.set(p)

    def on_scan(self):
        s, m, data = self.controller.scan_for_duplicates(self.path_var.get())
        if not s:
            messagebox.showwarning("Cảnh báo", m)
            return
            
        self.duplicates_data = data
        for i in self.tree.get_children(): self.tree.delete(i)
        
        count = 0
        for hash_val, paths in data.items():
            # The first file is kept as original, others as duplicates
            for i, p in enumerate(paths):
                if i == 0:
                    status = "⭐ Bản gốc"
                    tag = "original"
                else:
                    status = "❌ Bản sao"
                    tag = "duplicate"
                    count += 1
                
                size = f"{os.path.getsize(p) / 1024:.1f} KB"
                self.tree.insert("", tk.END, values=(status, p, size), tags=(tag,))
        
        self.tree.tag_configure("duplicate", background="#FFF3E0", foreground="#E65100") # Cam nhạt cho bản sao
        self.tree.tag_configure("original", background="#E8F5E9", foreground="#2E7D32") # Xanh nhạt cho bản gốc
        messagebox.showinfo("Xong", f"Tìm thấy {len(data)} nhóm trùng lặp ({count} bản sao).")


    def on_delete(self):
        if not self.duplicates_data:
            messagebox.showwarning("Cảnh báo", "Hãy quét file trước!")
            return
            
        to_delete = []
        for hash_val, paths in self.duplicates_data.items():
            to_delete.extend(paths[1:]) # Keep the first one
            
        if not to_delete:
            messagebox.showinfo("Thông báo", "Không có bản sao nào để xóa.")
            return
            
        if messagebox.askyesno("Xác nhận", f"Bạn có chắc muốn xóa {len(to_delete)} file bản sao?"):
            s, m, count = self.controller.delete_duplicates(to_delete)
            if s: messagebox.showinfo("Thành công", m)
            else: messagebox.showerror("Lỗi", m)
            self.on_scan() # Rescan
import os
