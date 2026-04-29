import tkinter as tk
from tkinter import messagebox, ttk
import json
import os
import sys
from .controller import AHKController

class AHKAutomationUI(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.controller = AHKController()
        
        # Đường dẫn file lưu cấu hình
        self.base_dir = os.path.dirname(os.path.abspath(sys.argv[0]))
        self.settings_file = os.path.join(self.base_dir, "ahk_settings.json")
        
        self.name_var = tk.StringVar()
        self.phone_var = tk.StringVar()
        self.email_var = tk.StringVar()
        self.address_var = tk.StringVar()
        
        # Tải dữ liệu cũ nếu có
        self.load_settings()
        
        self.setup_ui()
        self.update_status_label()

    def load_settings(self):
        """Tải thông tin từ file JSON"""
        if os.path.exists(self.settings_file):
            try:
                with open(self.settings_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    self.name_var.set(data.get("name", "Nguyen Van A"))
                    self.phone_var.set(data.get("phone", "0901234567"))
                    self.email_var.set(data.get("email", "contact@email.com"))
                    self.address_var.set(data.get("address", "123 Street, District 1, HCMC"))
            except:
                self.set_default_vars()
        else:
            self.set_default_vars()

    def set_default_vars(self):
        self.name_var.set("Nguyen Van A")
        self.phone_var.set("0901234567")
        self.email_var.set("contact@email.com")
        self.address_var.set("123 Street, District 1, HCMC")

    def save_settings(self):
        """Lưu thông tin hiện tại vào file JSON"""
        data = {
            "name": self.name_var.get(),
            "phone": self.phone_var.get(),
            "email": self.email_var.get(),
            "address": self.address_var.get()
        }
        try:
            with open(self.settings_file, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=4)
        except Exception as e:
            print(f"Lỗi lưu settings: {e}")


    def setup_ui(self):
        container = tk.Frame(self, padx=30, pady=30)
        container.pack(fill=tk.BOTH, expand=True)

        tk.Label(container, text="⌨️ AUTO HOTKEY AUTOMATION", font=("Arial", 16, "bold"), fg="#2C3E50").pack(pady=(0, 20))
        
        # Config Form
        form_frame = tk.LabelFrame(container, text=" Cấu hình thông tin cá nhân ", padx=20, pady=20, font=("Arial", 10, "bold"))
        form_frame.pack(fill=tk.X, pady=10)

        # Name
        tk.Label(form_frame, text="Họ và tên:").grid(row=0, column=0, sticky=tk.W, pady=5)
        tk.Entry(form_frame, textvariable=self.name_var, width=40).grid(row=0, column=1, padx=10, pady=5)

        # Phone
        tk.Label(form_frame, text="Số điện thoại:").grid(row=1, column=0, sticky=tk.W, pady=5)
        tk.Entry(form_frame, textvariable=self.phone_var, width=40).grid(row=1, column=1, padx=10, pady=5)

        # Email
        tk.Label(form_frame, text="Email:").grid(row=2, column=0, sticky=tk.W, pady=5)
        tk.Entry(form_frame, textvariable=self.email_var, width=40).grid(row=2, column=1, padx=10, pady=5)

        # Address
        tk.Label(form_frame, text="Địa chỉ:").grid(row=3, column=0, sticky=tk.W, pady=5)
        tk.Entry(form_frame, textvariable=self.address_var, width=40).grid(row=3, column=1, padx=10, pady=5)

        # Controls
        ctrl_frame = tk.Frame(container)
        ctrl_frame.pack(pady=20)

        self.btn_toggle = tk.Button(ctrl_frame, text="🚀 BẮT ĐẦU CHẠY", font=("Arial", 11, "bold"), 
                                   bg="#2ECC71", fg="white", width=20, height=2, command=self.on_toggle_click)
        self.btn_toggle.pack(side=tk.LEFT, padx=10)

        tk.Button(ctrl_frame, text="🛑 DỪNG TOOL", font=("Arial", 11, "bold"), 
                  bg="#E74C3C", fg="white", width=20, height=2, command=self.on_stop_click).pack(side=tk.LEFT, padx=10)

        # Status
        self.status_label = tk.Label(container, text="Trạng thái: Đang dừng", font=("Arial", 10, "italic"), fg="gray")
        self.status_label.pack(pady=10)

        # Quick Help
        help_frame = tk.LabelFrame(container, text=" Danh sách phím tắt nhanh ", padx=15, pady=15)
        help_frame.pack(fill=tk.BOTH, expand=True, pady=10)

        help_text = (
            "• F1: Menu công cụ nhanh\n"
            "• F2: Tự động điền Form (Tên, SĐT, Email)\n"
            "• F3: Bật/Tắt Auto Click\n"
            "• Alt + C/E/W/N: Mở Chrome/Excel/Word/Notepad\n"
            "• Ctrl+Shift+U: Chuyển HOA | Ctrl+Shift+V: Dán thuần\n"
            "• Alt + S: Tìm kiếm Google đoạn văn bản đã chọn"
        )
        tk.Label(help_frame, text=help_text, justify=tk.LEFT, font=("Arial", 9)).pack(anchor=tk.W)

    def on_toggle_click(self):
        config = {
            "name": self.name_var.get(),
            "phone": self.phone_var.get(),
            "email": self.email_var.get(),
            "address": self.address_var.get()
        }
        success, msg = self.controller.run_automation(config)
        if success:
            self.save_settings() # Lưu lại thông tin vào JSON
            messagebox.showinfo("Thành công", msg)
        else:

            messagebox.showerror("Lỗi", msg)
        self.update_status_label()

    def on_stop_click(self):
        success, msg = self.controller.stop_automation()
        if success:
            messagebox.showinfo("Đã dừng", msg)
        self.update_status_label()

    def update_status_label(self):
        is_running = self.controller.get_status()
        if is_running:
            self.status_label.config(text="Trạng thái: ĐANG CHẠY 🟢", fg="#27AE60")
            self.btn_toggle.config(text="🔄 CẬP NHẬT & CHẠY LẠI", bg="#3498DB")
        else:
            self.status_label.config(text="Trạng thái: ĐANG DỪNG 🔴", fg="#C0392B")
            self.btn_toggle.config(text="🚀 BẮT ĐẦU CHẠY", bg="#2ECC71")
        
        # Check status again after 2 seconds
        self.after(2000, self.update_status_label)
