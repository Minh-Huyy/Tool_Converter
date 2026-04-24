import sys
import tkinter as tk
from tkinterdnd2 import TkinterDnD

# Import modules
from core.dashboard import Dashboard
from modules.converter.ui import ConverterUI
from modules.organizer.ui import OrganizerUI
from modules.duplicate_finder.ui import DuplicateFinderUI
from modules.downloader.ui import DownloaderUI
from modules.compressor.ui import CompressorUI


class MultiToolApp:
    def __init__(self):
        self.root = TkinterDnD.Tk()
        self.root.title("Multi-Tool Utility Pro ⚙️")
        self.root.geometry("1100x600")
        
        self.dashboard = Dashboard(self.root)
        self.dashboard.pack(fill=tk.BOTH, expand=True)
        
        # Đăng ký các công cụ
        self.dashboard.register_tool("converter", ConverterUI)
        self.dashboard.register_tool("organizer", OrganizerUI)
        self.dashboard.register_tool("duplicate_finder", DuplicateFinderUI)
        self.dashboard.register_tool("downloader", DownloaderUI)
        self.dashboard.register_tool("compressor", CompressorUI)

        
        # Mở công cụ mặc định
        self.dashboard.switch_tool("converter")

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = MultiToolApp()
    app.run()
