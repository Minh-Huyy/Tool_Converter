import os
import sys
import win32com.client

def create_shortcut():
    try:
        # Path to the executable
        target = r"d:\Huy\Documents\Source_code\Project\Tool_Converter\dist\Multi_Tool_Utility\Multi_Tool_Utility.exe"
        if not os.path.exists(target):
            print(f"Error: Executable not found at {target}")
            return False

        # Path to the Desktop
        desktop = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')
        
        # Shortcut to update
        shortcuts = ["Multi-Tool Utility Pro.lnk"]

        shell = win32com.client.Dispatch("WScript.Shell")
        
        for s_name in shortcuts:
            path = os.path.join(desktop, s_name)
            shortcut = shell.CreateShortCut(path)
            shortcut.Targetpath = target
            shortcut.WorkingDirectory = os.path.dirname(target)
            shortcut.IconLocation = target
            shortcut.Description = "Multi-Tool Utility Pro for File Conversion, Organizing, and more."
            shortcut.save()
            print(f"Shortcut updated: {path}")

        return True
    except Exception as e:
        print(f"Error updating shortcuts: {e}")
        return False

if __name__ == "__main__":
    create_shortcut()
