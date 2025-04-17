# A Minimal Python App Launcher MEANT FOR PEOPLE WHO USE LIKE 34 PORTABLE BROWSERS. But I suppose you could do anything. With imagination. 

**Topper** is a lightweight, keyboard-driven app/program launcher written in Python with `tkinter`.  
It reads from a simple INI config, displays a frameless GUI list, supports tab/enter navigation, remembers your last selection, and launches your programs cleanly — even with fallback support if a path is missing.

![screenshot](https://raw.githubusercontent.com/whalelinguni/QuickLuncherBrowers/main/THIS.png)

---

## 🔧 Features

- INI-based configuration
- Tab and Shift+Tab to navigate
- Enter or double-click to launch
- Remembers last selection
- Optional `always_on_top` and `timeout` auto-close
- Clean fallback support (e.g., launches Minesweeper or Notepad if your path is broken)
- Opens `cmd` or `powershell` in a new window (no hijacking terminal)

---

## 🗂️ INI Format (`programs.ini`)

```ini
[options]
left_pad = 4
right_pad = 4
font = Consolas
font_size = 14
always_on_top = true
timeout = 15
remember_last = true

[programs]
Command Prompt = C:\Windows\System32\cmd.exe
PowerShell = C:\Windows\System32\WindowsPowerShell\v1.0\powershell.exe
Notepad = C:\Windows\System32\notepad.exe
```

---

## ▶️ Running the Script

Ensure you have Python 3 installed, then:

```bash
python Lunchers.py
```

You can also convert it to `.exe` using [PyInstaller](https://pyinstaller.org/) if you want to run it standalone.

---

## 📋 Notes

- The launcher window is centered and frameless by default.
- Selection is centered with optional padding.
- Paths are validated before launch.
- If a path is invalid or missing, it will fallback to launching:
  - `winmine.exe` if present (Windows 7)
  - Otherwise `notepad.exe`

---

## 🧩 TODO / Future Ideas

- Mouse hover to select
- Search bar for filtering
- Support `.lnk` shortcut resolution
- Portable mode with relative paths

---

## 🔒 License

MIT License. Use it, fork it, customize it.
```
