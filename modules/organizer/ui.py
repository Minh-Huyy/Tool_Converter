import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
from .controller import OrganizerController

class OrganizerUI(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.controller = OrganizerController()
        self.path_var = tk.StringVar()
        self.setup_ui()

    def setup_ui(self):
        main_frame = tk.Frame(self, padx=20, pady=20)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        tk.Label(main_frame, text="Chọn thư mục cần sắp xếp:", font=("Arial", 10, "bold")).pack(anchor=tk.W, pady=(0, 5))
        
        path_frame = tk.Frame(main_frame)
        path_frame.pack(fill=tk.X, pady=(0, 15))
        tk.Entry(path_frame, textvariable=self.path_var).pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))
        tk.Button(path_frame, text="📁 Chọn...", command=self.browse).pack(side=tk.RIGHT)
        
        tk.Button(main_frame, text="⚡ SẮP XẾP NGAY", font=("Arial", 11, "bold"),
                  bg="#2196F3", fg="white", command=self.on_click, width=30, height=2).pack(pady=10)
        
        tk.Label(main_frame, text="Nhật ký:", font=("Arial", 10, "bold")).pack(anchor=tk.W, pady=(10, 5))
        self.logs = scrolledtext.ScrolledText(main_frame, height=12, font=("Consolas", 9), state=tk.DISABLED)
        self.logs.pack(fill=tk.BOTH, expand=True)

    def browse(self):
        p = filedialog.askdirectory()
        if p: self.path_var.set(p)

    def on_click(self):
        s, m, l = self.controller.handle_organize(self.path_var.get())
        self.logs.config(state=tk.NORMAL)
        self.logs.delete(1.0, tk.END)
        for log in l: self.logs.insert(tk.END, log + "\n")
        if not l: self.logs.insert(tk.END, "Không có file nào.\n")
        self.logs.config(state=tk.DISABLED)
        if s: messagebox.showinfo("Xong", m)
        else: messagebox.showerror("Lỗi", m)
