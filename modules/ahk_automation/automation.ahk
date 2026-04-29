; ==============================================================================
; SCRIPT: Office & Study Automation Tool (Modular Version)
; ==============================================================================

#NoEnv
#SingleInstance Force
SendMode Input
SetWorkingDir %A_ScriptDir%

; === CONFIG SECTION (Dòng này sẽ được cập nhật tự động bởi Python) ===
global User_Name    := "Nguyen Van A"
global User_Phone   := "0901234567"
global User_Email   := "contact@email.com"
global User_Address := "123 Street, District 1, HCMC"
global User_Sign    := "Trân trọng,`n" . User_Name

; Trạng thái Auto Click
AutoClickStatus := false

; Thông báo khi chạy script
TrayTip, AutoHotkey Automation, Tool đã sẵn sàng hoạt động!, 3
return

; ==============================================================================
; 1. HOTSTRINGS (GÕ TẮT)
; ==============================================================================
::em@::
    SendInput %User_Email%
return

::sd@::
    SendInput %User_Phone%
return

::dc@::
    SendInput %User_Address%
return

::ck@::
    SendInput %User_Sign%
return

; ==============================================================================
; 2. PHÍM TẮT MỞ ỨNG DỤNG
; ==============================================================================
!c:: Run chrome.exe
!e:: Run excel.exe
!w:: Run winword.exe
!n:: Run notepad.exe

; ==============================================================================
; 3. AUTO NHẬP FORM (F2)
; ==============================================================================
F2::
    ToolTip, Đang điền form...
    SendInput %User_Name%
    Sleep 300
    Send {Tab}
    Sleep 300
    SendInput %User_Phone%
    Sleep 300
    Send {Tab}
    Sleep 300
    SendInput %User_Email%
    Sleep 300
    Send {Tab}
    Sleep 300
    SendInput %User_Address%
    ToolTip
return

; ==============================================================================
; 4. TEXT PROCESSING
; ==============================================================================
^+u::
    ClipSaved := ClipboardAll
    Clipboard := ""
    Send ^c
    ClipWait, 1
    if ErrorLevel
        return
    StringUpper, Clipboard, Clipboard
    Send ^v
    Sleep 100
    Clipboard := ClipSaved
return

^+v::
    Clipboard := Clipboard
    Send ^v
return

; ==============================================================================
; 5. AUTOMATION CƠ BẢN (F3)
; ==============================================================================
F3::
    AutoClickStatus := !AutoClickStatus
    if (AutoClickStatus) {
        ToolTip, Auto Click: ON
        SetTimer, DoClick, 100
    } else {
        ToolTip, Auto Click: OFF
        SetTimer, DoClick, Off
        Sleep 1000
        ToolTip
    }
return

DoClick:
    Click
return

; ==============================================================================
; 6. TÌM KIẾM NHANH (Alt + S)
; ==============================================================================
!s::
    ClipSaved := ClipboardAll
    Clipboard := ""
    Send ^c
    ClipWait, 1
    if !ErrorLevel {
        Run, https://www.google.com/search?q=%Clipboard%
    }
    Clipboard := ClipSaved
return

; ==============================================================================
; 7. MENU TOOL (F1)
; ==============================================================================
; Thêm lệnh cho phép kéo thả GUI bằng chuột trái
OnMessage(0x0201, "WM_LBUTTONDOWN")

F1::
    Gui, Destroy
    Gui, +AlwaysOnTop -Caption +Border
    Gui, Margin, 20, 20
    Gui, Color, FFFFFF ; Nền trắng cho sạch
    Gui, Font, s12 Bold, Segoe UI
    Gui, Add, Text, x10 y10 w200 Center, QUICK TOOLS MENU
    
    Gui, Font, s10 Normal
    Gui, Add, Button, gOpenChrome w180 h30, [Alt+C] Mở Chrome
    Gui, Add, Button, gOpenExcel w180 h30, [Alt+E] Mở Excel
    Gui, Add, Button, gCopyEmail w180 h30, Copy Email
    Gui, Add, Button, gCopyPhone w180 h30, Copy SĐT
    Gui, Add, Button, gGuiClose w180 h30, Đóng (Esc)
    
    Gui, Show, , QuickMenu
return

WM_LBUTTONDOWN() {
    if (A_Gui = "")
        return
    PostMessage, 0xA1, 2,,, A ; Lệnh Windows cho phép nắm kéo cửa sổ
}

OpenChrome:
    Run chrome.exe
    Gui, Destroy
return

OpenExcel:
    Run excel.exe
    Gui, Destroy
return

CopyEmail:
    Clipboard := User_Email
    ToolTip, Đã copy Email
    Sleep 1000
    ToolTip
    Gui, Destroy
return

CopyPhone:
    Clipboard := User_Phone
    ToolTip, Đã copy SĐT
    Sleep 1000
    ToolTip
    Gui, Destroy
return

GuiEscape:
GuiClose:
    Gui, Destroy
return

; ==============================================================================
; 8. CONTEXT-AWARE (Chrome)
; ==============================================================================
#IfWinActive ahk_exe chrome.exe
F4::
    Send ^w
    ToolTip, Đã đóng tab Chrome
    SetTimer, RemoveToolTip, -1000
return
#IfWinActive

RemoveToolTip:
    ToolTip
return
