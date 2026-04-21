import os
import sys
import tkinter as tk
from tkinter import filedialog, messagebox, ttk

# Kiểm tra thư viện từ khi phần mềm vừa khởi động
try:
    from PIL import Image
    from pydub import AudioSegment
except ImportError as e:
    print(f"[LOI] Thieu thu vien moi truong. Chi tiet: {e}")
    print("Vui long chay lenh tren Terminal: pip install Pillow pydub pyaudioop")
    sys.exit(1)

# Import module nội tại
from controller import ConverterController

class FileConverterUI:
    def __init__(self, root, controller):
        self.root = root
        self.controller = controller
        
        self.root.title("Multi File Converter Tool ⚙️")
        self.root.geometry("520x340")
        self.root.resizable(False, False)
        
        self.input_var = tk.StringVar()
        self.output_var = tk.StringVar()
        self.format_var = tk.StringVar()
        
        self.setup_ui()
        
    def setup_ui(self):
        main_frame = tk.Frame(self.root, padx=20, pady=20)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        tk.Label(main_frame, text="File đầu vào (Input):", font=("Arial", 10, "bold")).grid(row=0, column=0, sticky=tk.W, pady=(0, 5))
        
        self.input_entry = tk.Entry(main_frame, textvariable=self.input_var, width=45, state="readonly", justify='left')
        self.input_entry.grid(row=1, column=0, padx=(0, 5), pady=(0, 15))
        
        btn_browse_in = tk.Button(main_frame, text="📂 Chọn...", command=self.browse_input)
        btn_browse_in.grid(row=1, column=1, pady=(0, 15))

        tk.Label(main_frame, text="Chọn định dạng đích muốn convert:", font=("Arial", 10, "bold")).grid(row=2, column=0, sticky=tk.W, pady=(0, 5))
        
        self.format_combo = ttk.Combobox(main_frame, textvariable=self.format_var, state="readonly", width=42)
        self.format_combo.grid(row=3, column=0, padx=(0, 5), pady=(0, 15))
        self.format_combo.bind("<<ComboboxSelected>>", self.on_format_change)

        tk.Label(main_frame, text="Lưu thành (Đường dẫn kết quả):", font=("Arial", 10, "bold")).grid(row=4, column=0, sticky=tk.W, pady=(0, 5))
        
        self.output_entry = tk.Entry(main_frame, textvariable=self.output_var, width=45)
        self.output_entry.grid(row=5, column=0, padx=(0, 5), pady=(0, 20))
        
        btn_browse_out = tk.Button(main_frame, text="📁 Chọn...", command=self.browse_output)
        btn_browse_out.grid(row=5, column=1, pady=(0, 20))

        btn_convert = tk.Button(main_frame, text="🚀 BẮT ĐẦU CONVERT", font=("Arial", 11, "bold"), 
                                bg="#4CAF50", fg="white", activebackground="#45a049", activeforeground="white",
                                command=self.on_convert_click, width=25, height=2)
        btn_convert.grid(row=6, column=0, columnspan=2, pady=5)
        
    def browse_input(self):
        file_path = filedialog.askopenfilename(
            title="Chọn file muốn chuyển đổi",
            filetypes=(
                ("Tất cả mức hỗ trợ", "*.jpg *.jpeg *.png *.webp *.mp3 *.wav *.ogg"),
                ("Ảnh (Images)", "*.jpg *.jpeg *.png *.webp"),
                ("Âm thanh (Audio)", "*.mp3 *.wav *.ogg"),
                ("All files", "*.*")
            )
        )
        
        if file_path:
            self.input_var.set(file_path)
            
            _, file_name = os.path.split(file_path)
            _, ext = os.path.splitext(file_name)
            ext_lower = ext.lower()
            
            if ext_lower in [".jpg", ".jpeg", ".png", ".webp", ".bmp"]:
                self.format_combo['values'] = ("png", "jpg", "webp")
                self.format_var.set("png" if ext_lower in [".jpg", ".jpeg"] else "jpg")
            elif ext_lower in [".mp3", ".wav", ".ogg", ".flac"]:
                self.format_combo['values'] = ("mp3", "wav", "ogg")
                self.format_var.set("mp3" if ext_lower != ".mp3" else "wav")
            else:
                self.format_combo['values'] = ()
                self.format_var.set("")
                
            self.update_output_path()
            
    def on_format_change(self, event=None):
        self.update_output_path()
        
    def update_output_path(self):
        in_path = self.input_var.get()
        target_ext = self.format_var.get()
        
        if not in_path or not target_ext:
            return
            
        dir_name, file_name = os.path.split(in_path)
        name_only, _ = os.path.splitext(file_name)
        
        suggested_out = os.path.join(dir_name, f"{name_only}_converted.{target_ext}")
        self.output_var.set(suggested_out)
            
    def browse_output(self):
        file_path = filedialog.asksaveasfilename(
            title="Lưu file chuyển đổi thành",
            defaultextension=".*",
            filetypes=(
                ("Tùy chọn ghi thủ công", "*.*"),
                ("PNG image", "*.png"),
                ("JPEG image", "*.jpg"),
                ("WEBP image", "*.webp"),
                ("MP3 audio", "*.mp3"),
                ("WAV audio", "*.wav"),
                ("OGG audio", "*.ogg"),
            )
        )
        if file_path:
            self.output_var.set(file_path)
            
    def on_convert_click(self):
        in_path = self.input_var.get()
        out_path = self.output_var.get()
        
        if not in_path or not out_path:
            messagebox.showwarning("Cảnh báo", "Bạn phải nhập đủ 2 khung đường dẫn!")
            return
            
        success, message = self.controller.handle_convert(in_path, out_path)
        
        if success:
            messagebox.showinfo("Thành công", message)
        else:
            messagebox.showerror("Báo Lỗi", message)

if __name__ == "__main__":
    root = tk.Tk()
    app_controller = ConverterController()
    app_ui = FileConverterUI(root, controller=app_controller)
    root.mainloop()
