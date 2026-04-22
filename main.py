import os
import sys
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from tkinterdnd2 import TkinterDnD, DND_FILES

# Kiểm tra thư viện từ khi phần mềm vừa khởi động
try:
    from PIL import Image, ImageTk
    from pydub import AudioSegment
    import docx
    import docx2pdf
    import pdf2docx
    import PyPDF2
    import pygame
except ImportError as e:
    print(f"[LOI] Thieu thu vien moi truong. Chi tiet: {e}")
    print("Vui long chay lenh tren Terminal: pip install Pillow pydub pyaudioop docx2pdf pdf2docx python-docx PyPDF2 pygame-ce")
    sys.exit(1)

# Import module nội tại
from controller import ConverterController

class FileConverterUI:
    def __init__(self, root, controller):
        self.root = root
        self.controller = controller
        
        self.root.title("Multi File Converter Tool ⚙️")
        self.root.geometry("850x380")
        self.root.resizable(False, False)
        
        self.input_var = tk.StringVar()
        self.output_var = tk.StringVar()
        self.format_var = tk.StringVar()
        
        try:
            pygame.mixer.init()
        except:
            pass
        self.audio_playing = False
        
        self.setup_ui()
        
    def setup_ui(self):
        main_layout = tk.Frame(self.root)
        main_layout.pack(fill=tk.BOTH, expand=True)
        
        main_frame = tk.Frame(main_layout, padx=20, pady=20)
        main_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        preview_container = tk.Frame(main_layout, padx=10, pady=20, width=320)
        preview_container.pack(side=tk.RIGHT, fill=tk.Y)
        preview_container.pack_propagate(False)
        
        tk.Label(preview_container, text="XEM TRƯỚC (PREVIEW)", font=("Arial", 10, "bold"), fg="#555").pack(pady=(0, 10))
        
        self.preview_frame = tk.Frame(preview_container, bg="white", relief=tk.SUNKEN, bd=1)
        self.preview_frame.pack(fill=tk.BOTH, expand=True)
        
        # Setup form ui
        
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
        
        # Thêm ghi chú dưới UI
        tk.Label(main_frame, text="(Hoặc kéo thả file trực tiếp vào cửa sổ này)", font=("Arial", 9, "italic"), fg="gray").grid(row=7, column=0, columnspan=2, pady=(10, 0))
        
        # Cho phép kéo thả vào root window và main_frame
        self.root.drop_target_register(DND_FILES)
        self.root.dnd_bind('<<Drop>>', self.on_drop_file)
        
        main_frame.drop_target_register(DND_FILES)
        main_frame.dnd_bind('<<Drop>>', self.on_drop_file)
        
        self.input_entry.drop_target_register(DND_FILES)
        self.input_entry.dnd_bind('<<Drop>>', self.on_drop_file)
        
    def browse_input(self):
        file_path = filedialog.askopenfilename(
            title="Chọn file muốn chuyển đổi",
            filetypes=(
                ("Tất cả mức hỗ trợ", "*.jpg *.jpeg *.png *.webp *.mp3 *.wav *.ogg *.docx *.pdf"),
                ("Ảnh (Images)", "*.jpg *.jpeg *.png *.webp"),
                ("Âm thanh (Audio)", "*.mp3 *.wav *.ogg"),
                ("Tài liệu (Documents)", "*.docx *.pdf"),
                ("All files", "*.*")
            )
        )
        
        if file_path:
            self.process_input_file(file_path)
            
    def on_drop_file(self, event):
        file_path = event.data
        if file_path.startswith('{') and file_path.endswith('}'):
            file_path = file_path[1:-1]
        self.process_input_file(file_path)

    def process_input_file(self, file_path):
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
        elif ext_lower == ".docx":
            self.format_combo['values'] = ("pdf", "txt")
            self.format_var.set("pdf")
        elif ext_lower == ".pdf":
            self.format_combo['values'] = ("docx", "txt")
            self.format_var.set("docx")
        else:
            self.format_combo['values'] = ()
            self.format_var.set("")
            
        self.update_output_path()
        self.update_preview()
        
    def update_preview(self):
        # Dọn dẹp preview pane
        for widget in self.preview_frame.winfo_children():
            widget.destroy()
            
        if self.audio_playing:
            pygame.mixer.music.stop()
            self.audio_playing = False
            
        in_path = self.input_var.get()
        if not in_path or not os.path.exists(in_path):
            tk.Label(self.preview_frame, text="Chưa có thông tin", bg="white", fg="gray").pack(expand=True)
            return
            
        ext_lower = os.path.splitext(in_path)[1].lower()
        
        try:
            if ext_lower in [".jpg", ".jpeg", ".png", ".webp", ".bmp"]:
                img = Image.open(in_path)
                img.thumbnail((290, 240))
                self.preview_img = ImageTk.PhotoImage(img) # Giữ reference
                lbl_img = tk.Label(self.preview_frame, image=self.preview_img, bg="white")
                lbl_img.pack(expand=True, pady=10)
                tk.Label(self.preview_frame, text=f"Kích thước: {img.size[0]}x{img.size[1]}", bg="white", font=("Arial", 9)).pack()
                
            elif ext_lower in [".docx", ".pdf", ".txt"]:
                text_widget = tk.Text(self.preview_frame, wrap=tk.WORD, bg="#fafafa", font=("Arial", 9))
                text_widget.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
                
                content = ""
                if ext_lower == ".docx":
                    doc = docx.Document(in_path)
                    content = "\n".join([p.text for p in doc.paragraphs[:15]])
                elif ext_lower == ".pdf":
                    reader = PyPDF2.PdfReader(in_path)
                    if len(reader.pages) > 0:
                        content = reader.pages[0].extract_text()
                elif ext_lower == ".txt":
                    with open(in_path, "r", encoding="utf-8") as f:
                        content = f.read(1000)
                        
                text_widget.insert(tk.END, content[:800] + ("..." if len(content) > 800 else ""))
                text_widget.config(state=tk.DISABLED)
                
            elif ext_lower in [".mp3", ".wav", ".ogg", ".flac"]:
                tk.Label(self.preview_frame, text="🎶 Tệp Âm Thanh", bg="white", font=("Arial", 12, "bold"), fg="#2196F3").pack(pady=(40, 10))
                size_mb = os.path.getsize(in_path) / (1024*1024)
                tk.Label(self.preview_frame, text=f"Dung lượng: {size_mb:.2f} MB", bg="white").pack()
                
                btn_play = tk.Button(self.preview_frame, text="▶ Phát thử (Play)", font=("Arial", 10), bg="#E0E0E0", width=15)
                btn_play.pack(pady=20)
                
                def toggle_play():
                    if not self.audio_playing:
                        pygame.mixer.music.load(in_path)
                        pygame.mixer.music.play()
                        self.audio_playing = True
                        btn_play.config(text="⏹ Dừng (Stop)")
                    else:
                        pygame.mixer.music.stop()
                        self.audio_playing = False
                        btn_play.config(text="▶ Phát thử (Play)")
                        
                btn_play.config(command=toggle_play)
            else:
                tk.Label(self.preview_frame, text="Định dạng chưa có Preview", bg="white", fg="gray").pack(expand=True)
        except Exception as e:
            tk.Label(self.preview_frame, text=f"Lỗi tải Preview:\n{str(e)}", bg="white", fg="red").pack(expand=True)
            
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
                ("PDF document", "*.pdf"),
                ("Word document", "*.docx"),
                ("Text file", "*.txt"),
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
    root = TkinterDnD.Tk()
    app_controller = ConverterController()
    app_ui = FileConverterUI(root, controller=app_controller)
    root.mainloop()
