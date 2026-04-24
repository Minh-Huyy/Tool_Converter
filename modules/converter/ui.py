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
        
        self.input_files = []
        self.output_dir_var = tk.StringVar()
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
        tk.Label(main_frame, text="Danh sách file đầu vào (Input Files):", font=("Arial", 10, "bold")).grid(row=0, column=0, sticky=tk.W, pady=(0, 5))
        
        list_container = tk.Frame(main_frame)
        list_container.grid(row=1, column=0, padx=(0, 5), pady=(0, 15), sticky="nsew")
        
        self.file_listbox = tk.Listbox(list_container, width=45, height=8, font=("Arial", 9))
        self.file_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        sb = tk.Scrollbar(list_container, orient="vertical", command=self.file_listbox.yview)
        sb.pack(side=tk.RIGHT, fill=tk.Y)
        self.file_listbox.config(yscrollcommand=sb.set)
        self.file_listbox.bind("<<ListboxSelect>>", lambda e: self.update_preview())

        btn_list_frame = tk.Frame(main_frame)
        btn_list_frame.grid(row=1, column=1, sticky="n", pady=(0, 15))
        tk.Button(btn_list_frame, text="📂 Thêm file", command=self.browse_input, width=12).pack(pady=2)
        tk.Button(btn_list_frame, text="❌ Xóa hết", command=self.clear_list, width=12).pack(pady=2)

        tk.Label(main_frame, text="Chọn định dạng đích (Target Format):", font=("Arial", 10, "bold")).grid(row=2, column=0, sticky=tk.W, pady=(0, 5))
        self.format_combo = ttk.Combobox(main_frame, textvariable=self.format_var, state="readonly", width=42)
        self.format_combo.grid(row=3, column=0, padx=(0, 5), pady=(0, 15))

        tk.Label(main_frame, text="Lưu tại thư mục (Output Folder):", font=("Arial", 10, "bold")).grid(row=4, column=0, sticky=tk.W, pady=(0, 5))
        self.output_entry = tk.Entry(main_frame, textvariable=self.output_dir_var, width=45)
        self.output_entry.grid(row=5, column=0, padx=(0, 5), pady=(0, 20))
        tk.Button(main_frame, text="📁 Chọn...", command=self.browse_output).grid(row=5, column=1, pady=(0, 20))

        tk.Button(main_frame, text="🚀 BẮT ĐẦU BATCH CONVERT", font=("Arial", 11, "bold"), 
                  bg="#4CAF50", fg="white", command=self.on_convert_click, width=30, height=2).grid(row=6, column=0, columnspan=2, pady=5)
        
        tk.Label(main_frame, text="(Kéo thả nhiều file vào đây)", font=("Arial", 9, "italic"), fg="gray").grid(row=7, column=0, columnspan=2, pady=(10, 0))
        
        # Drag & Drop
        self.drop_target_register(DND_FILES)
        self.dnd_bind('<<Drop>>', self.on_drop_file)

    def browse_input(self):
        files = filedialog.askopenfilenames(title="Chọn các file", filetypes=(("Tất cả", "*.jpg *.jpeg *.png *.webp *.mp3 *.wav *.ogg *.docx *.pdf"), ("All files", "*.*")))
        if files:
            self.process_input_files(list(files))
            
    def on_drop_file(self, event):
        data = event.data
        # Parse paths correctly (handles spaces and braces)
        import re
        paths = re.findall(r'\{.*?\}|\S+', data)
        paths = [p[1:-1] if p.startswith('{') and p.endswith('}') else p for p in paths]
        self.process_input_files(paths)

    def process_input_files(self, file_paths):
        for fp in file_paths:
            if os.path.isfile(fp) and fp not in self.input_files:
                self.input_files.append(fp)
                self.file_listbox.insert(tk.END, os.path.basename(fp))
        
        if self.input_files:
            # Update format options based on the first file
            self.update_format_options(self.input_files[0])
            # Auto set output dir if empty
            if not self.output_dir_var.get():
                self.output_dir_var.set(os.path.dirname(self.input_files[0]))
            self.update_preview()

    def update_format_options(self, sample_file):
        ext = os.path.splitext(sample_file)[1].lower()
        if ext in [".jpg", ".jpeg", ".png", ".webp", ".bmp"]:
            self.format_combo['values'] = ("png", "jpg", "webp")
            if not self.format_var.get(): self.format_var.set("png" if ext in [".jpg", ".jpeg"] else "jpg")
        elif ext in [".mp3", ".wav", ".ogg", ".flac"]:
            self.format_combo['values'] = ("mp3", "wav", "ogg")
            if not self.format_var.get(): self.format_var.set("mp3" if ext != ".mp3" else "wav")
        elif ext == ".docx":
            self.format_combo['values'] = ("pdf", "txt")
            if not self.format_var.get(): self.format_var.set("pdf")
        elif ext == ".pdf":
            self.format_combo['values'] = ("docx", "txt")
            if not self.format_var.get(): self.format_var.set("docx")

    def clear_list(self):
        self.input_files = []
        self.file_listbox.delete(0, tk.END)
        self.update_preview()

    def browse_output(self):
        path = filedialog.askdirectory(title="Chọn thư mục lưu")
        if path: self.output_dir_var.set(path)

    def update_preview(self):
        for widget in self.preview_frame.winfo_children(): widget.destroy()
        if self.audio_playing:
            try: pygame.mixer.music.stop(); self.audio_playing = False
            except: pass
            
        selection = self.file_listbox.curselection()
        if not selection and not self.input_files:
            tk.Label(self.preview_frame, text="Chưa có file nào", bg="white", fg="gray").pack(expand=True)
            return
            
        idx = selection[0] if selection else 0
        if idx >= len(self.input_files): return
        
        in_path = self.input_files[idx]
        if not os.path.exists(in_path):
            tk.Label(self.preview_frame, text="File không tồn tại", bg="white", fg="red").pack(expand=True)
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
                tk.Label(self.preview_frame, text=f"File: {os.path.basename(in_path)}", bg="white", wraplength=250).pack(expand=True)
        except Exception as e:
            tk.Label(self.preview_frame, text=f"Lỗi preview: {e}", bg="white", fg="red", wraplength=250).pack(expand=True)

    def toggle_play(self, path, btn):
        try:
            if not self.audio_playing:
                pygame.mixer.music.load(path); pygame.mixer.music.play()
                self.audio_playing = True; btn.config(text="⏹ Stop")
            else:
                pygame.mixer.music.stop(); self.audio_playing = False; btn.config(text="▶ Play")
        except: pass

    def on_convert_click(self):
        if not self.input_files:
            messagebox.showwarning("Cảnh báo", "Vui lòng thêm file vào danh sách!")
            return
        if not self.output_dir_var.get():
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn thư mục lưu!")
            return
            
        s, m = self.controller.handle_batch_convert(
            self.input_files, 
            self.output_dir_var.get(), 
            self.format_var.get()
        )
        if s: messagebox.showinfo("Thành công", m)
        else: messagebox.showerror("Lỗi", m)
