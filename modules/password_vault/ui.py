import tkinter as tk
from tkinter import ttk, messagebox
from .controller import PasswordVaultController

class PasswordVaultUI(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg="white")
        self.controller = PasswordVaultController()
        self.current_account_id = None
        
        self.setup_ui()

    def setup_ui(self):
        # Clear frame
        for widget in self.winfo_children():
            widget.destroy()

        if not self.controller.is_vault_ready():
            self.show_setup_screen()
        else:
            self.show_login_screen()

    def show_setup_screen(self):
        container = tk.Frame(self, bg="white", padx=40, pady=40)
        container.place(relx=0.5, rely=0.4, anchor="center")

        tk.Label(container, text="🛡️ Thiết lập Password Vault", font=("Arial", 22, "bold"), bg="white", fg="#2C3E50").pack(pady=(0, 20))
        tk.Label(container, text="Đây là lần đầu bạn sử dụng. Vui lòng tạo mật khẩu chủ.\nLưu ý: Nếu quên mật khẩu này, bạn sẽ mất toàn bộ dữ liệu!", 
                 bg="white", fg="#7F8C8D", justify="center").pack(pady=(0, 20))

        tk.Label(container, text="Mật khẩu chủ mới:", bg="white", font=("Arial", 10)).pack(anchor="w")
        self.master_pass_entry = tk.Entry(container, font=("Arial", 12), show="*", width=35)
        self.master_pass_entry.pack(pady=(5, 20))

        btn_setup = tk.Button(
            container, text="KÍCH HOẠT VAULT", bg="#27AE60", fg="white", 
            font=("Arial", 12, "bold"), padx=20, pady=10, cursor="hand2", border=0,
            command=self.handle_setup
        )
        btn_setup.pack(fill=tk.X)

    def show_login_screen(self):
        container = tk.Frame(self, bg="white", padx=40, pady=40)
        container.place(relx=0.5, rely=0.4, anchor="center")

        tk.Label(container, text="🔐 Password Vault", font=("Arial", 24, "bold"), bg="white", fg="#2C3E50").pack(pady=(0, 20))
        
        tk.Label(container, text="Nhập mật khẩu chủ để mở khóa:", bg="white", font=("Arial", 10)).pack(anchor="w")
        self.login_entry = tk.Entry(container, font=("Arial", 14), show="*", width=30)
        self.login_entry.pack(pady=(5, 20))
        self.login_entry.bind("<Return>", lambda e: self.handle_login())

        btn_login = tk.Button(
            container, text="MỞ KHÓA", bg="#3498DB", fg="white", 
            font=("Arial", 12, "bold"), padx=20, pady=10, cursor="hand2", border=0,
            command=self.handle_login
        )
        btn_login.pack(fill=tk.X)

    def handle_setup(self):
        pwd = self.master_pass_entry.get()
        if len(pwd) < 4:
            messagebox.showwarning("Cảnh báo", "Mật khẩu chủ phải có ít nhất 4 ký tự.")
            return
        
        if self.controller.setup_vault(pwd):
            messagebox.showinfo("Thành công", "Vault đã được tạo và kích hoạt!")
            self.show_main_vault()
        else:
            messagebox.showerror("Lỗi", "Không thể khởi tạo vault.")

    def handle_login(self):
        pwd = self.login_entry.get()
        if self.controller.unlock_vault(pwd):
            self.show_main_vault()
        else:
            messagebox.showerror("Lỗi", "Mật khẩu chủ không chính xác!")

    def show_main_vault(self):
        for widget in self.winfo_children():
            widget.destroy()

        # Layout: Top bar, Sidebar (list), Detail area
        # Top Bar
        top_bar = tk.Frame(self, bg="#F8F9FA", height=60)
        top_bar.pack(fill=tk.X)
        top_bar.pack_propagate(False)

        tk.Label(top_bar, text="🔑 Password Vault Pro", font=("Arial", 16, "bold"), bg="#F8F9FA", fg="#2C3E50").pack(side=tk.LEFT, padx=20)
        
        # Search
        search_frame = tk.Frame(top_bar, bg="#F8F9FA")
        search_frame.pack(side=tk.LEFT, padx=40)
        tk.Label(search_frame, text="🔍", bg="#F8F9FA").pack(side=tk.LEFT)
        self.search_var = tk.StringVar()
        self.search_var.trace_add("write", lambda *args: self.refresh_list())
        search_entry = tk.Entry(search_frame, textvariable=self.search_var, font=("Arial", 11), width=30)
        search_entry.pack(side=tk.LEFT, padx=5)

        btn_add = tk.Button(top_bar, text="+ THÊM TÀI KHOẢN", bg="#27AE60", fg="white", font=("Arial", 10, "bold"), 
                            padx=15, border=0, cursor="hand2", command=self.open_add_dialog)
        btn_add.pack(side=tk.RIGHT, padx=20, pady=10)

        # Main Body
        body = tk.Frame(self, bg="white")
        body.pack(fill=tk.BOTH, expand=True)

        # Sidebar List
        self.sidebar = tk.Frame(body, bg="white", width=300, borderwidth=1, relief="solid")
        self.sidebar.pack(side=tk.LEFT, fill=tk.Y)
        self.sidebar.pack_propagate(False)

        self.account_list = tk.Listbox(self.sidebar, font=("Arial", 11), border=0, selectbackground="#E3F2FD", selectforeground="black", activestyle="none")
        self.account_list.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        self.account_list.bind("<<ListboxSelect>>", self.on_account_select)

        # Detail Panel
        self.detail_panel = tk.Frame(body, bg="white", padx=30, pady=30)
        self.detail_panel.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.refresh_list()
        self.show_empty_detail()

    def refresh_list(self):
        self.account_list.delete(0, tk.END)
        self.accounts = self.controller.get_accounts(self.search_var.get())
        for acc in self.accounts:
            self.account_list.insert(tk.END, acc['site'])

    def show_empty_detail(self):
        for widget in self.detail_panel.winfo_children():
            widget.destroy()
        tk.Label(self.detail_panel, text="Chọn một tài khoản để xem chi tiết", font=("Arial", 12), bg="white", fg="#95A5A6").place(relx=0.5, rely=0.4, anchor="center")

    def on_account_select(self, event):
        selection = self.account_list.curselection()
        if not selection:
            return
        
        index = selection[0]
        account = self.accounts[index]
        self.current_account_id = account["id"]
        self.show_account_details(account)

    def show_account_details(self, account):
        for widget in self.detail_panel.winfo_children():
            widget.destroy()

        tk.Label(self.detail_panel, text=account["site"], font=("Arial", 20, "bold"), bg="white", fg="#2C3E50").pack(anchor="w", pady=(0, 20))

        # Fields
        self.create_detail_field("Tên đăng nhập:", account["username"], copy_btn=True)
        self.create_detail_field("Mật khẩu:", account["password"], is_password=True, copy_btn=True)
        self.create_detail_field("Ghi chú:", account["notes"] if account["notes"] else "---")

        # Actions
        btn_frame = tk.Frame(self.detail_panel, bg="white")
        btn_frame.pack(anchor="w", pady=30)

        tk.Button(btn_frame, text="Chỉnh sửa", bg="#F39C12", fg="white", font=("Arial", 10, "bold"), padx=15, pady=5, border=0, cursor="hand2", 
                  command=lambda: self.open_edit_dialog(account)).pack(side=tk.LEFT, marginRight=10)
        tk.Button(btn_frame, text="Xóa tài khoản", bg="#E74C3C", fg="white", font=("Arial", 10, "bold"), padx=15, pady=5, border=0, cursor="hand2",
                  command=lambda: self.handle_delete(account["id"])).pack(side=tk.LEFT, padx=10)

    def create_detail_field(self, label_text, value_text, is_password=False, copy_btn=False):
        frame = tk.Frame(self.detail_panel, bg="white")
        frame.pack(fill=tk.X, pady=5)
        
        tk.Label(frame, text=label_text, font=("Arial", 10, "bold"), bg="white", fg="#7F8C8D", width=15, anchor="w").pack(side=tk.LEFT)
        
        display_val = "••••••••" if is_password else value_text
        val_label = tk.Label(frame, text=display_val, font=("Arial", 11), bg="white", fg="#2C3E50")
        val_label.pack(side=tk.LEFT, padx=10)

        if is_password:
            def toggle():
                if val_label.cget("text") == "••••••••":
                    val_label.config(text=value_text)
                    btn_toggle.config(text="Ẩn")
                else:
                    val_label.config(text="••••••••")
                    btn_toggle.config(text="Hiện")
            
            btn_toggle = tk.Button(frame, text="Hiện", font=("Arial", 8), bg="#ECF0F1", border=0, command=toggle)
            btn_toggle.pack(side=tk.LEFT, padx=5)

        if copy_btn:
            tk.Button(frame, text="Sao chép", font=("Arial", 8), bg="#ECF0F1", border=0, 
                      command=lambda: self.controller.copy_to_clipboard(value_text)).pack(side=tk.LEFT, padx=5)

    def open_add_dialog(self):
        self.show_account_form()

    def open_edit_dialog(self, account):
        self.show_account_form(account)

    def show_account_form(self, account=None):
        dialog = tk.Toplevel(self)
        dialog.title("Thêm/Sửa tài khoản" if not account else "Cập nhật tài khoản")
        dialog.geometry("450x550")
        dialog.configure(bg="white")
        dialog.grab_set()

        container = tk.Frame(dialog, bg="white", padx=20, pady=20)
        container.pack(fill=tk.BOTH, expand=True)

        tk.Label(container, text="Thông tin tài khoản", font=("Arial", 14, "bold"), bg="white").pack(pady=(0, 20))

        tk.Label(container, text="Trang web / Dịch vụ:", bg="white").pack(anchor="w")
        # Sử dụng Combobox để gợi ý các dịch vụ đã có
        existing_sites = sorted(list(set(acc['site'] for acc in self.controller.get_accounts())))
        site_entry = ttk.Combobox(container, font=("Arial", 11), width=38, values=existing_sites)
        site_entry.pack(pady=(5, 15))
        if account: site_entry.set(account["site"])

        tk.Label(container, text="Tên đăng nhập / Email:", bg="white").pack(anchor="w")
        user_entry = tk.Entry(container, font=("Arial", 11), width=40)
        user_entry.pack(pady=(5, 15))
        if account: user_entry.insert(0, account["username"])

        tk.Label(container, text="Mật khẩu:", bg="white").pack(anchor="w")
        pass_frame = tk.Frame(container, bg="white")
        pass_frame.pack(fill=tk.X, pady=(5, 15))
        pass_entry = tk.Entry(pass_frame, font=("Arial", 11), width=28)
        pass_entry.pack(side=tk.LEFT)
        if account: pass_entry.insert(0, account["password"])

        def gen_pass():
            new_p = self.controller.generate_strong_password()
            pass_entry.delete(0, tk.END)
            pass_entry.insert(0, new_p)
        
        tk.Button(pass_frame, text="Tạo mới", font=("Arial", 9), bg="#3498DB", fg="white", border=0, command=gen_pass).pack(side=tk.LEFT, padx=5)

        tk.Label(container, text="Ghi chú:", bg="white").pack(anchor="w")
        notes_text = tk.Text(container, font=("Arial", 11), height=4, width=40)
        notes_text.pack(pady=(5, 20))
        if account: notes_text.insert("1.0", account["notes"])

        def save():
            site = site_entry.get()
            user = user_entry.get()
            pwd = pass_entry.get()
            notes = notes_text.get("1.0", tk.END).strip()

            if account:
                success, msg = self.controller.update_account(account["id"], site, user, pwd, notes)
            else:
                success, msg = self.controller.add_account(site, user, pwd, notes)
            
            if success:
                messagebox.showinfo("Thành công", msg)
                dialog.destroy()
                self.refresh_list()
                # If editing, refresh detail view
                if account:
                    self.show_account_details({"id": account["id"], "site": site, "username": user, "password": pwd, "notes": notes})
            else:
                messagebox.showwarning("Lỗi", msg)

        tk.Button(container, text="LƯU THÔNG TIN", bg="#27AE60", fg="white", font=("Arial", 12, "bold"), pady=10, border=0, command=save).pack(fill=tk.X)

    def handle_delete(self, acc_id):
        if messagebox.askyesno("Xác nhận", "Bạn có chắc chắn muốn xóa tài khoản này?"):
            if self.controller.delete_account(acc_id):
                messagebox.showinfo("Thành công", "Đã xóa tài khoản.")
                self.refresh_list()
                self.show_empty_detail()
