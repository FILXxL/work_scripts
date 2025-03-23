import subprocess
from tkinter import messagebox

def run_command(command, shell=True):
    try:
        result = subprocess.run(command, shell=shell, capture_output=True, text=True)
        if result.returncode != 0:
            messagebox.showerror("Fehler", f"Fehler bei der Ausführung:\n{result.stderr}")
            return False
        return True
    except Exception as e:
        messagebox.showerror("Fehler", f"Ein Fehler ist aufgetreten:\n{str(e)}")
        return False 