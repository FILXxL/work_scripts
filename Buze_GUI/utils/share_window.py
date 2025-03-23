import customtkinter as ctk # type: ignore
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
    
    # Connect button
    def connect_share():
        import subprocess
        import os
        
        selected = center_menu.get()[:3]
        drive = drive_entry.get().strip()
        
        if not drive.endswith(':'):
            drive += ':'
        
        # Silently try to delete existing mapping
        subprocess.run(f'net use {drive} /delete', shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        
        # Different path for Teesdorf
        if selected == "TDF":
            share_path = "\\\\n3000\\tt"
        else:
            share_path = f"\\\\atlas\\ftgroups\\{selected}"
        
        # Try to map the new drive
        run_command(f'net use {drive} "{share_path}"')
        
        # Verify the drive is actually mapped and accessible
        if os.path.exists(f"{drive}\\"):
            messagebox.showinfo("Erfolg", f"Zentrumsordner wurde als {drive} verbunden.")
            share_window.destroy()
        else:
            messagebox.showerror("Fehler", f"Zentrumsordner konnte nicht als {drive} verbunden werden.")
    
    ctk.CTkButton(
        main_frame,
        text="Verbinden",
        command=connect_share,
        width=120,
        height=32
    ).pack(pady=20) 