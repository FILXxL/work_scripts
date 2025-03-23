import tkinter as tk
from tkinter import ttk, messagebox
from utils.commands import run_command

def create_printer_window(parent, selected_center, selected_center_full, printers, zentrum):
    printer_window = tk.Toplevel(parent)
    printer_window.title(f"Drucker für {selected_center_full}")
    printer_window.geometry("400x300")
    
    frame = ttk.Frame(printer_window, padding="20")
    frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
    
    ttk.Label(frame, text=f"Verfügbare Drucker in {selected_center_full}:", 
             font=('Helvetica', 10, 'bold')).grid(row=0, column=0, pady=(0, 10))
    
    printer_listbox = tk.Listbox(frame, selectmode=tk.MULTIPLE, width=40, height=10)
    printer_listbox.grid(row=1, column=0, pady=(0, 10))
    
    scrollbar = ttk.Scrollbar(frame, orient="vertical", command=printer_listbox.yview)
    scrollbar.grid(row=1, column=1, sticky=(tk.N, tk.S))
    printer_listbox.configure(yscrollcommand=scrollbar.set)
    
    for printer in printers:
        printer_listbox.insert(tk.END, printer)
    
    def install_selected_printers():
        selections = printer_listbox.curselection()
        if not selections:
            messagebox.showwarning("Warnung", "Bitte wählen Sie mindestens einen Drucker aus.")
            return
        
        server = f"n{zentrum.get()}"
        success_count = 0
        
        for index in selections:
            printer_name = printer_listbox.get(index)
            command = f'RUNDLL32 printui.dll,PrintUIEntry /in /n "\\\\{server}\\{printer_name}"'
            if run_command(command):
                success_count += 1
        
        if success_count > 0:
            messagebox.showinfo("Erfolg", f"{success_count} Drucker wurde(n) erfolgreich hinzugefügt.")
        printer_window.destroy()
    
    ttk.Button(frame, text="Ausgewählte Drucker installieren", 
              command=install_selected_printers,
              width=30).grid(row=2, column=0, pady=15) 