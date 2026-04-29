import tkinter as tk
from tkinter import ttk

class Dashboard(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.current_tool = None
        self.tools = {}
        self.setup_ui()

    def setup_ui(self):
        # Sidebar
        self.sidebar = tk.Frame(self, bg="#2C3E50", width=200)
        self.sidebar.pack(side=tk.LEFT, fill=tk.Y)
        self.sidebar.pack_propagate(False)
        
        tk.Label(self.sidebar, text="🛠️ UTILITY HUB", font=("Arial", 14, "bold"), bg="#2C3E50", fg="white", pady=20).pack()
        
        # Tool Buttons
        self.add_nav_button("🔄 Converter", "converter")
        self.add_nav_button("📂 Organizer", "organizer")
        self.add_nav_button("🔍 Duplicate Finder", "duplicate_finder")
        self.add_nav_button("⬇️ Downloader", "downloader")
        self.add_nav_button("📦 Compressor", "compressor")
        self.add_nav_button("🔐 Password Vault", "password_vault")
        self.add_nav_button("⌨️ AHK Automation", "ahk_automation")
        
        # Content Area
        self.content_area = tk.Frame(self, bg="white")
        self.content_area.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

    def add_nav_button(self, text, tool_id):
        btn = tk.Button(self.sidebar, text=text, font=("Arial", 10), bg="#34495E", fg="white", 
                        relief=tk.FLAT, pady=10, cursor="hand2", anchor="w", padx=20,
                        command=lambda: self.switch_tool(tool_id))
        btn.pack(fill=tk.X, pady=1)
        btn.bind("<Enter>", lambda e: btn.config(bg="#1ABC9C"))
        btn.bind("<Leave>", lambda e: btn.config(bg="#34495E"))

    def register_tool(self, tool_id, tool_class):
        self.tools[tool_id] = tool_class

    def switch_tool(self, tool_id):
        if self.current_tool:
            self.current_tool.pack_forget()
        
        if tool_id in self.tools:
            tool_class = self.tools[tool_id]
            self.current_tool = tool_class(self.content_area)
            self.current_tool.pack(fill=tk.BOTH, expand=True)
