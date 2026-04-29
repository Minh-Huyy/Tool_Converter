import os
import subprocess
import sys

def resource_path(relative_path):
    """ Lấy đường dẫn tuyệt đối đến tài nguyên, hoạt động cho cả dev và PyInstaller """
    if hasattr(sys, '_MEIPASS'):
        # Chạy từ file .exe đóng gói bởi PyInstaller
        base_path = sys._MEIPASS
    else:
        # Chạy từ mã nguồn (.py), lấy thư mục chứa file main.py
        base_path = os.path.dirname(os.path.abspath(sys.argv[0]))

    return os.path.join(base_path, relative_path)

class AHKService:
    def __init__(self):
        # File gốc (Template) - nằm trong bộ đóng gói
        self.template_path = resource_path(os.path.join("modules", "ahk_automation", "automation.ahk"))
        
        # File thực thi (Active) - nằm ở thư mục làm việc hiện tại để có quyền ghi
        self.base_dir = os.path.dirname(os.path.abspath(sys.argv[0]))
        self.script_path = os.path.join(self.base_dir, "active_automation.ahk")
        
        # Đường dẫn đến bản AHK Portable trong thư mục bin
        self.ahk_exe_path = resource_path(os.path.join("bin", "AutoHotkey.exe"))
        self.process = None

    def update_script_config(self, config):
        """Đọc từ template, thay thế thông tin và ghi ra file active_automation.ahk"""
        if not os.path.exists(self.template_path):
            return False, "Không tìm thấy file template automation.ahk"
        
        try:
            with open(self.template_path, 'r', encoding='utf-8-sig') as f:
                lines = f.readlines()
            
            new_lines = []
            for line in lines:
                if line.startswith("global User_Name"):
                    new_lines.append(f'global User_Name    := "{config.get("name", "")}"\n')
                elif line.startswith("global User_Phone"):
                    new_lines.append(f'global User_Phone   := "{config.get("phone", "")}"\n')
                elif line.startswith("global User_Email"):
                    new_lines.append(f'global User_Email   := "{config.get("email", "")}"\n')
                elif line.startswith("global User_Address"):
                    new_lines.append(f'global User_Address := "{config.get("address", "")}"\n')
                else:
                    new_lines.append(line)

            # Ghi ra file active (luôn nằm ở thư mục gốc của dự án)
            with open(self.script_path, 'w', encoding='utf-8-sig') as f:
                f.writelines(new_lines)
            
            return True, "Cập nhật cấu hình thành công"
        except Exception as e:
            return False, f"Lỗi cập nhật script: {str(e)}"

    def start_script(self):
        """Chạy script AHK từ file active_automation.ahk"""
        if self.is_running():
            self.stop_script() # Đóng cái cũ trước khi chạy cái mới

        try:
            # 1. Kiểm tra bản Portable trong bin
            if os.path.exists(self.ahk_exe_path):
                self.process = subprocess.Popen([self.ahk_exe_path, self.script_path])
                return True, "Đã khởi chạy bằng AHK Portable"
            
            # 2. Nếu không có Portable, thử chạy trực tiếp
            self.process = subprocess.Popen([self.script_path], shell=True)
            return True, "Đã khởi chạy script AHK (System)"
        except Exception as e:
            return False, f"Không thể khởi chạy script: {str(e)}"

    def stop_script(self):
        """Dừng script AHK bằng cách đóng process."""
        try:
            # Cách an toàn nhất trong AHK là dùng lệnh reload hoặc exit từ bên trong, 
            # nhưng ở đây ta sẽ dùng taskkill để đơn giản.
            subprocess.run(["taskkill", "/F", "/IM", "AutoHotkey.exe"], capture_output=True)
            self.process = None
            return True, "Đã dừng script AHK"
        except Exception as e:
            return False, f"Lỗi khi dừng script: {str(e)}"

    def is_running(self):
        """Kiểm tra xem AutoHotkey có đang chạy không."""
        try:
            output = subprocess.check_output('tasklist /FI "IMAGENAME eq AutoHotkey.exe"', shell=True).decode()
            return "AutoHotkey.exe" in output
        except:
            return False
