import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from utils.commands import run_command

def create_share_window(parent, center_names):
    share_window = tk.Toplevel(parent)
    share_window.title("Zusätzliches Zentrum hinzufügen")
    share_window.geometry("400x200")
    
    frame = ttk.Frame(share_window, padding="20")
    frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
    
    ttk.Label(frame, text="Zentrum auswählen:", 
             font=('Helvetica', 10, 'bold')).grid(row=0, column=0, pady=(0, 10))
    
    center_display_values = [f"{abbr} - {name}" for abbr, name in center_names.items()]
    
    additional_zentrum = ttk.Combobox(frame, 
                                    values=center_display_values,
                                    state='readonly')
    additional_zentrum.grid(row=1, column=0, pady=(0, 20))
    
    def process_selection():
        selected_zentrum = additional_zentrum.get()[:3]
        if not selected_zentrum:
            messagebox.showwarning("Warnung", "Bitte wählen Sie ein Zentrum aus.")
            return
        
        zentrum_map = {
            'SFD': '3110', 'MLK': '3130', 'OOE': '3140',
            'TRL': '3160', 'LEB': '3180', 'KAL': '3280',
            'KTN': '3190', 'TDF': '3000'
        }
        
        drive_letter = simpledialog.askstring("Laufwerk", 
                                            "Laufwerksbuchstabe für zusätzlichen Zentrumsordner (z.B. Z:):",
                                            parent=share_window)
        
        if drive_letter:
            if not drive_letter.endswith(':'): 
                drive_letter += ':'
            
            run_command(f'net use {drive_letter} /delete')
            
            if zentrum_map[selected_zentrum] == "3000":
                command = f'net use {drive_letter} \\\\n3000\\tt'
            else:
                command = f'net use {drive_letter} \\\\atlas\\ftgroups\\{zentrum_map[selected_zentrum]}'
            
            if run_command(command):
                messagebox.showinfo("Erfolg", 
                                  f"Zusätzlicher Zentrumsordner wurde als {drive_letter} eingerichtet.")
                share_window.destroy()
    
    ttk.Button(frame, text="Weiter", 
               command=process_selection).grid(row=2, column=0, pady=10) 