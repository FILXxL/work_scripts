import customtkinter as ctk
from tkinter import messagebox
from utils.commands import run_command

def create_share_window(parent, center_names):
    share_window = ctk.CTkToplevel(parent)
    share_window.title("Zusätzlichen Zentrumsordner verbinden")
    share_window.geometry("500x300")
    share_window.grab_set()  # Make window modal
    
    # Main frame with padding
    main_frame = ctk.CTkFrame(share_window)
    main_frame.pack(fill="both", expand=True, padx=20, pady=20)
    
    # Title
    ctk.CTkLabel(
        main_frame,
        text="Zentrumsordner verbinden",
        font=ctk.CTkFont(size=16, weight="bold")
    ).pack(pady=(0, 20))
    
    # Center selection
    center_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
    center_frame.pack(fill="x", pady=(0, 20))
    
    ctk.CTkLabel(
        center_frame,
        text="Zentrum:",
        font=ctk.CTkFont(size=12)
    ).pack(side="left", padx=(0, 10))
    
    center_values = [f"{abbr} - {name}" for abbr, name in center_names.items()]
    center_menu = ctk.CTkOptionMenu(
        center_frame,
        values=center_values,
        width=300
    )
    center_menu.pack(side="left")
    
    # Drive letter entry
    drive_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
    drive_frame.pack(fill="x", pady=(0, 20))
    
    ctk.CTkLabel(
        drive_frame,
        text="Laufwerksbuchstabe:",
        font=ctk.CTkFont(size=12)
    ).pack(side="left", padx=(0, 10))
    
    drive_entry = ctk.CTkEntry(drive_frame, width=50)
    drive_entry.pack(side="left")
    drive_entry.insert(0, "X:")
    
    # Connect button
    def connect_share():
        selected = center_menu.get()[:3]
        drive = drive_entry.get().strip()
        
        if not drive.endswith(':'):
            drive += ':'
        
        run_command(f'net use {drive} /delete')
        if run_command(f'net use {drive} "\\\\atlas\\ftgroups\\{selected}"'):
            messagebox.showinfo("Erfolg", f"Zentrumsordner wurde als {drive} verbunden.")
            share_window.destroy()
    
    ctk.CTkButton(
        main_frame,
        text="Verbinden",
        command=connect_share,
        width=120,
        height=32
    ).pack(pady=20) 