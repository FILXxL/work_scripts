import customtkinter as ctk
from tkinter import messagebox
from utils.commands import run_command

def create_printer_window(parent, center, center_full, printers, zentrum):
    printer_window = ctk.CTkToplevel(parent)
    printer_window.title(f"Drucker für {center_full}")
    printer_window.geometry("500x400")
    printer_window.grab_set()  # Make window modal
    
    # Main frame with padding
    main_frame = ctk.CTkFrame(printer_window)
    main_frame.pack(fill="both", expand=True, padx=20, pady=20)
    
    # Title
    ctk.CTkLabel(
        main_frame,
        text=f"Verfügbare Drucker für {center}",
        font=ctk.CTkFont(size=16, weight="bold")
    ).pack(pady=(0, 20))
    
    # Create scrollable frame for printers
    scroll_frame = ctk.CTkScrollableFrame(main_frame)
    scroll_frame.pack(fill="both", expand=True)
    
    # Checkboxes for printers
    printer_vars = {}
    for printer in printers:
        var = ctk.BooleanVar()
        printer_vars[printer] = var
        
        checkbox = ctk.CTkCheckBox(
            scroll_frame,
            text=printer,
            variable=var,
            font=ctk.CTkFont(size=12)
        )
        checkbox.pack(pady=5, padx=10, anchor="w")
    
    # Buttons frame
    button_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
    button_frame.pack(fill="x", pady=(20, 0))
    
    # Select All button
    def select_all():
        for var in printer_vars.values():
            var.set(True)
    
    ctk.CTkButton(
        button_frame,
        text="Alle auswählen",
        command=select_all,
        width=120,
        height=32
    ).pack(side="left", padx=5)
    
    # Install button
    def install_printers():
        selected = [printer for printer, var in printer_vars.items() if var.get()]
        if not selected:
            messagebox.showwarning("Warnung", "Bitte wählen Sie mindestens einen Drucker aus.")
            return
        
        for printer in selected:
            command = f'RUNDLL32 printui.dll,PrintUIEntry /in /n "\\\\{zentrum.get()}\\{printer}"'
            run_command(command)
        
        messagebox.showinfo("Erfolg", "Die ausgewählten Drucker wurden installiert.")
        printer_window.destroy()
    
    ctk.CTkButton(
        button_frame,
        text="Installieren",
        command=install_printers,
        width=120,
        height=32
    ).pack(side="right", padx=5) 