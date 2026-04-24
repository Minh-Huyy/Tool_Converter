import os
import win32com.client

def check_shortcut(path):
    try:
        shell = win32com.client.Dispatch("WScript.Shell")
        shortcut = shell.CreateShortCut(path)
        print(f"Shortcut: {os.path.basename(path)}")
        print(f"Target: {shortcut.Targetpath}")
        print("-" * 20)
    except Exception as e:
        print(f"Error checking {path}: {e}")

if __name__ == "__main__":
    desktop = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')
    check_shortcut(os.path.join(desktop, "Multi-Tool Utility Hub.lnk"))
    check_shortcut(os.path.join(desktop, "Multi-Tool Utility Pro.lnk"))
