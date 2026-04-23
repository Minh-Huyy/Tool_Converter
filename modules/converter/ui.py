import os
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from tkinterdnd2 import DND_FILES
from PIL import Image, ImageTk
try:
    import pygame
except ImportError:
    pass

from .controller import ConverterController

class ConverterUI(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.controller = ConverterController()
        
        self.input_var = tk.StringVar()
        self.output_var = tk.StringVar()
        self.format_var = tk.StringVar()
        
        self.audio_playing = False
        self.setup_ui()
        
    def setup_ui(self):
        main_layout = tk.Frame(self)
        main_layout.pack(fill=tk.BOTH, expand=True)
        
        main_frame = tk.Frame(main_layout, padx=20, pady=20)
        main_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        preview_container = tk.Frame(main_layout, padx=10, pady=20, width=320)
        preview_container.pack(side=tk.RIGHT, fill=tk.Y)
        preview_container.pack_propagate(False)
        
        tk.Label(preview_container, text="XEM TRƯỚC (PREVIEW)", font=("Arial", 10, "bold"), fg="#555").pack(pady=(0, 10))
        self.preview_frame = tk.Frame(preview_container, bg="white", relief=tk.SUNKEN, bd=1)
        self.preview_frame.pack(fill=tk.BOTH, expand=True)
        
        # Form
        tk.Label(main_frame, text="File đầu vào (Input):", font=("Arial", 10, "bold")).grid(row=0, column=0, sticky=tk.W, pady=(0, 5))
        self.input_entry = tk.Entry(main_frame, textvariable=self.input_var, width=45, state="readonly")
        self.input_entry.grid(row=1, column=0, padx=(0, 5), pady=(0, 15))
        tk.Button(main_frame, text="📂 Chọn...", command=self.browse_input).grid(row=1, column=1, pady=(0, 15))

        tk.Label(main_frame, text="Chọn định dạng đích:", font=("Arial", 10, "bold")).grid(row=2, column=0, sticky=tk.W, pady=(0, 5))
        self.format_combo = ttk.Combobox(main_frame, textvariable=self.format_var, state="readonly", width=42)
        self.format_combo.grid(row=3, column=0, padx=(0, 5), pady=(0, 15))
        self.format_combo.bind("<<ComboboxSelected>>", lambda e: self.update_output_path())

        tk.Label(main_frame, text="Lưu thành:", font=("Arial", 10, "bold")).grid(row=4, column=0, sticky=tk.W, pady=(0, 5))
        self.output_entry = tk.Entry(main_frame, textvariable=self.output_var, width=45)
        self.output_entry.grid(row=5, column=0, padx=(0, 5), pady=(0, 20))
        tk.Button(main_frame, text="📁 Chọn...", command=self.browse_output).grid(row=5, column=1, pady=(0, 20))

        tk.Button(main_frame, text="🚀 BẮT ĐẦU CONVERT", font=("Arial", 11, "bold"), 
                  bg="#4CAF50", fg="white", command=self.on_convert_click, width=25, height=2).grid(row=6, column=0, columnspan=2, pady=5)
        
        tk.Label(main_frame, text="(Kéo thả file vào đây)", font=("Arial", 9, "italic"), fg="gray").grid(row=7, column=0, columnspan=2, pady=(10, 0))
        
        # Drag & Drop
        self.drop_target_register(DND_FILES)
        self.dnd_bind('<<Drop>>', self.on_drop_file)

    def browse_input(self):
        file_path = filedialog.askopenfilename(title="Chọn file", filetypes=(("Tất cả", "*.jpg *.jpeg *.png *.webp *.mp3 *.wav *.ogg *.docx *.pdf"), ("All files", "*.*")))
        if file_path: self.process_input_file(file_path)
            
    def on_drop_file(self, event):
        file_path = event.data
        if file_path.startswith('{') and file_path.endswith('}'): file_path = file_path[1:-1]
        self.process_input_file(file_path)

    def process_input_file(self, file_path):
        self.input_var.set(file_path)
        ext = os.path.splitext(file_path)[1].lower()
        if ext in [".jpg", ".jpeg", ".png", ".webp", ".bmp"]:
            self.format_combo['values'] = ("png", "jpg", "webp")
            self.format_var.set("png" if ext in [".jpg", ".jpeg"] else "jpg")
        elif ext in [".mp3", ".wav", ".ogg", ".flac"]:
            self.format_combo['values'] = ("mp3", "wav", "ogg")
            self.format_var.set("mp3" if ext != ".mp3" else "wav")
        elif ext == ".docx":
            self.format_combo['values'] = ("pdf", "txt"); self.format_var.set("pdf")
        elif ext == ".pdf":
            self.format_combo['values'] = ("docx", "txt"); self.format_var.set("docx")
        self.update_output_path()
        self.update_preview()

    def update_output_path(self):
        in_path = self.input_var.get()
        target_ext = self.format_var.get()
        if in_path and target_ext:
            dir_name, file_name = os.path.split(in_path)
            name_only, _ = os.path.splitext(file_name)
            self.output_var.set(os.path.join(dir_name, f"{name_only}_converted.{target_ext}"))

    def browse_output(self):
        file_path = filedialog.asksaveasfilename(title="Lưu file", defaultextension=".*")
        if file_path: self.output_var.set(file_path)

    def update_preview(self):
        for widget in self.preview_frame.winfo_children(): widget.destroy()
        if self.audio_playing:
            try: pygame.mixer.music.stop(); self.audio_playing = False
            except: pass
            
        in_path = self.input_var.get()
        if not in_path or not os.path.exists(in_path):
            tk.Label(self.preview_frame, text="Chưa có thông tin", bg="white", fg="gray").pack(expand=True)
            return
            
        ext = os.path.splitext(in_path)[1].lower()
        try:
            if ext in [".jpg", ".jpeg", ".png", ".webp", ".bmp"]:
                img = Image.open(in_path)
                img.thumbnail((290, 240))
                self.preview_img = ImageTk.PhotoImage(img)
                tk.Label(self.preview_frame, image=self.preview_img, bg="white").pack(expand=True, pady=10)
            elif ext in [".mp3", ".wav", ".ogg", ".flac"]:
                tk.Label(self.preview_frame, text="🎶 Audio File", bg="white", font=("Arial", 12, "bold")).pack(pady=40)
                btn = tk.Button(self.preview_frame, text="▶ Play", command=lambda: self.toggle_play(in_path, btn))
                btn.pack(pady=20)
            else:
                tk.Label(self.preview_frame, text="No Preview", bg="white").pack(expand=True)
        except Exception as e:
            tk.Label(self.preview_frame, text=f"Lỗi: {e}", bg="white", fg="red").pack(expand=True)

    def toggle_play(self, path, btn):
        try:
            if not self.audio_playing:
                pygame.mixer.music.load(path); pygame.mixer.music.play()
                self.audio_playing = True; btn.config(text="⏹ Stop")
            else:
                pygame.mixer.music.stop(); self.audio_playing = False; btn.config(text="▶ Play")
        except: pass

    def on_convert_click(self):
        s, m = self.controller.handle_convert(self.input_var.get(), self.output_var.get())
        if s: messagebox.showinfo("Thành công", m)
        else: messagebox.showerror("Lỗi", m)
