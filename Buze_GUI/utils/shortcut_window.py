import customtkinter as ctk # type: ignore
from tkinter import messagebox
import os
from pathlib import Path
from utils.commands import run_command

def create_shortcut_window(parent):
    shortcut_window = ctk.CTkToplevel(parent)
    shortcut_window.title("Desktop-Verknüpfungen erstellen")
    shortcut_window.geometry("500x400")
    shortcut_window.grab_set()  # Make window modal
    
    # Main frame with padding
    main_frame = ctk.CTkFrame(shortcut_window)
    main_frame.pack(fill="both", expand=True, padx=20, pady=20)
    
    # Title
    ctk.CTkLabel(
        main_frame,
        text="Verfügbare Verknüpfungen",
        font=ctk.CTkFont(size=16, weight="bold")
    ).pack(pady=(0, 20))
    
    # Create scrollable frame for shortcuts
    scroll_frame = ctk.CTkScrollableFrame(main_frame)
    scroll_frame.pack(fill="both", expand=True)
    
    # Define available shortcuts
    shortcuts = {
        "Outlook": r"C:\Program Files\Microsoft Office\root\Office16\OUTLOOK.EXE",
        "Excel": r"C:\Program Files\Microsoft Office\root\Office16\EXCEL.EXE",
        "Word": r"C:\Program Files\Microsoft Office\root\Office16\WINWORD.EXE",
        "Chrome": r"C:\Program Files\Google\Chrome\Application\chrome.exe",
        "Firefox": r"C:\Program Files\Mozilla Firefox\firefox.exe"
    }
    
    # Checkboxes for shortcuts
    shortcut_vars = {}
    for name, path in shortcuts.items():
        if os.path.exists(path):
            var = ctk.BooleanVar()
            shortcut_vars[name] = (var, path)
            
            checkbox = ctk.CTkCheckBox(
                scroll_frame,
                text=name,
                variable=var,
                font=ctk.CTkFont(size=12)
            )
            checkbox.pack(pady=5, padx=10, anchor="w")
    
    # Buttons frame
    button_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
    button_frame.pack(fill="x", pady=(20, 0))
    
    # Select All button
    def select_all():
        for var, _ in shortcut_vars.values():
            var.set(True)
    
    ctk.CTkButton(
        button_frame,
        text="Alle auswählen",
        command=select_all,
        width=120,
        height=32
    ).pack(side="left", padx=5)
    
    # Create shortcuts button
    def create_shortcuts():
        selected = [(name, path) for name, (var, path) in shortcut_vars.items() if var.get()]
        if not selected:
            messagebox.showwarning("Warnung", "Bitte wählen Sie mindestens eine Verknüpfung aus.")
            return
        
        desktop = str(Path.home() / "Desktop")
        for name, path in selected:
            command = f'powershell "$ws = New-Object -ComObject WScript.Shell; $s = $ws.CreateShortcut(\'{desktop}\\{name}.lnk\'); $s.TargetPath = \'{path}\'; $s.Save()"'
            run_command(command)
        
        messagebox.showinfo("Erfolg", "Die ausgewählten Verknüpfungen wurden erstellt.")
        shortcut_window.destroy()
    
    ctk.CTkButton(
        button_frame,
        text="Erstellen",
        command=create_shortcuts,
        width=120,
        height=32
    ).pack(side="right", padx=5) 