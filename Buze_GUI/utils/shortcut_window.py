import tkinter as tk
from tkinter import ttk, messagebox
import os
from pathlib import Path
from config.shortcuts import SHORTCUTS

def create_shortcut_window(parent):
    shortcut_window = tk.Toplevel(parent)
    shortcut_window.title("Desktop-Verknüpfungen")
    shortcut_window.geometry("400x300")
    
    # Make window modal
    shortcut_window.transient(parent)
    shortcut_window.grab_set()
    
    frame = ttk.Frame(shortcut_window, padding="20")
    frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
    
    ttk.Label(frame, text="Verfügbare Verknüpfungen:", 
             font=('Helvetica', 10, 'bold')).grid(row=0, column=0, pady=(0, 10))
    
    # Create a listbox with available shortcuts
    shortcut_listbox = tk.Listbox(frame, selectmode=tk.MULTIPLE, width=40, height=10)
    shortcut_listbox.grid(row=1, column=0, pady=(0, 10))
    
    # Add scrollbar
    scrollbar = ttk.Scrollbar(frame, orient="vertical", command=shortcut_listbox.yview)
    scrollbar.grid(row=1, column=1, sticky=(tk.N, tk.S))
    shortcut_listbox.configure(yscrollcommand=scrollbar.set)
    
    # Insert shortcuts
    for shortcut_name in SHORTCUTS:
        shortcut_listbox.insert(tk.END, shortcut_name)
    
    def create_selected_shortcuts():
        selections = shortcut_listbox.curselection()
        if not selections:
            messagebox.showwarning("Warnung", "Bitte wählen Sie mindestens eine Verknüpfung aus.")
            return
        
        desktop_path = str(Path.home() / "Desktop")
        success_count = 0
        
        for index in selections:
            shortcut_name = shortcut_listbox.get(index)
            shortcut_info = SHORTCUTS[shortcut_name]
            
            if shortcut_info.get("type") == "outlook_shortcut":
                # Use the path from the configuration
                outlook_source = shortcut_info["path"]
                if os.path.exists(outlook_source):
                    os.system(f'copy "{outlook_source}" "{desktop_path}"')
                    success_count += 1
                else:
                    messagebox.showwarning("Warnung", 
                                         "Outlook-Verknüpfung konnte nicht gefunden werden.")
            else:
                # Handle URL shortcuts
                shortcut_path = os.path.join(desktop_path, shortcut_info["name"])
                try:
                    with open(shortcut_path, 'w') as f:
                        f.write(f"[InternetShortcut]\nURL={shortcut_info['url']}")
                    success_count += 1
                except Exception as e:
                    messagebox.showerror("Fehler", 
                                       f"Fehler beim Erstellen von {shortcut_name}: {str(e)}")
        
        if success_count > 0:
            messagebox.showinfo("Erfolg", 
                              f"{success_count} Verknüpfung(en) wurde(n) erfolgreich erstellt.")
        shortcut_window.destroy()
    
    # Add create button
    ttk.Button(frame, text="Ausgewählte Verknüpfungen erstellen", 
              command=create_selected_shortcuts,
              width=30).grid(row=2, column=0, pady=15) 