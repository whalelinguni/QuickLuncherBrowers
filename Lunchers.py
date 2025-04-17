import configparser
import os
import subprocess
import tkinter as tk
from tkinter import messagebox

# === Load INI ===
script_dir = os.path.dirname(os.path.abspath(__file__))
ini_path = os.path.join(script_dir, "programs.ini")

config = configparser.ConfigParser()
config.read(ini_path)

if "programs" not in config:
    raise ValueError("No [programs] section in INI file.")

last_path = os.path.join(script_dir, ".topper_last")
remember_last = config.get("options", "remember_last", fallback="false").lower() in ("1", "true", "yes")
last_selected_name = None

if remember_last and os.path.exists(last_path):
    with open(last_path, "r", encoding="utf-8") as f:
        last_selected_name = f.read().strip()

# === Options ===
left_pad = int(config.get("options", "left_pad", fallback=0))
right_pad = int(config.get("options", "right_pad", fallback=0))
font_family = config.get("options", "font", fallback="Consolas")
font_size = int(config.get("options", "font_size", fallback=12))
always_on_top = config.get("options", "always_on_top", fallback="false").lower() in ("1", "true", "yes")
timeout_seconds = int(config.get("options", "timeout", fallback=0))

# === Programs ===
raw_programs = list(config["programs"].items())
all_programs = raw_programs + [("", ""), ("Exit", "EXIT")]

# === Padding (no centering hacks) ===
max_len = max(len(name) for name, _ in all_programs) + left_pad + right_pad
padded_programs = []
for name, path in all_programs:
    padded_name = f"{' ' * left_pad}{name}{' ' * right_pad}"
    padded_programs.append((padded_name, path))

# === GUI ===
def launch_selected(event=None):
    selection = listbox.curselection()
    if selection:
        selected_name, path = padded_programs[selection[0]]
        if path == "EXIT":
            root.destroy()
            return
        if not os.path.exists(path):
            fallback = "C:\\Windows\\System32\\winmine.exe"
            if not os.path.exists(fallback):
                fallback = "C:\\Windows\\System32\\notepad.exe"
            path = fallback
        try:
            #subprocess.Popen(path, shell=True, creationflags=subprocess.CREATE_NEW_CONSOLE)
            if os.path.basename(path).lower() in ("cmd.exe", "powershell.exe"):
                subprocess.Popen(f'start "" "{path}"', shell=True)
            else:
                subprocess.Popen(path, shell=True, creationflags=subprocess.CREATE_NEW_CONSOLE)
                

            # Save last-used selection
            if remember_last:
                with open(last_path, "w", encoding="utf-8") as f:
                    f.write(selected_name.strip())

            root.destroy()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to launch:\n{e}")

def tab_forward(event):
    current = listbox.curselection()
    index = (current[0] + 1) % len(padded_programs) if current else 0
    listbox.selection_clear(0, tk.END)
    listbox.selection_set(index)
    listbox.activate(index)
    return "break"

def tab_backward(event):
    current = listbox.curselection()
    index = (current[0] - 1) % len(padded_programs) if current else len(padded_programs) - 1
    listbox.selection_clear(0, tk.END)
    listbox.selection_set(index)
    listbox.activate(index)
    return "break"

def auto_close():
    root.destroy()

# === Init Window ===
root = tk.Tk()
root.overrideredirect(True)
root.configure(bg="black")
root.attributes("-topmost", always_on_top)

listbox = tk.Listbox(
    root,
    width=max_len,
    height=len(padded_programs),
    font=(font_family, font_size),
    activestyle='dotbox',
    justify='center',
    bg="black",
    fg="white",
    bd=0,
    highlightthickness=0,
    selectbackground="#444444",
    selectforeground="white"
)
listbox.pack(padx=10, pady=10)

# === Populate and restore last selection if any ===
for idx, (name, _) in enumerate(padded_programs):
    listbox.insert(tk.END, name)
    if remember_last and last_selected_name and name.strip() == last_selected_name:
        last_index = idx

listbox.focus_set()
if remember_last and 'last_index' in locals():
    listbox.selection_set(last_index)
    listbox.activate(last_index)
else:
    listbox.selection_set(0)
    listbox.activate(0)

# === Bindings ===
listbox.bind("<Return>", launch_selected)
listbox.bind("<Double-1>", launch_selected)
listbox.bind("<Escape>", lambda e: root.destroy())
listbox.bind("<Tab>", tab_forward)
listbox.bind("<Shift-Tab>", tab_backward)

# === Center on screen ===
root.update_idletasks()
w = root.winfo_width()
h = root.winfo_height()
x = (root.winfo_screenwidth() // 2) - (w // 2)
y = (root.winfo_screenheight() // 2) - (h // 2)
root.geometry(f'{w}x{h}+{x}+{y}')

# === Timeout support ===
if timeout_seconds > 0:
    root.after(timeout_seconds * 1000, auto_close)

root.mainloop()
