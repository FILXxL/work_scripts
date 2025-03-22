import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import os
import subprocess
from pathlib import Path
import winreg

class BuzeGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("ÖAMTC Fahrtechnik Onboarding")
        self.root.geometry("800x600")
        
        # Variables
        self.zentrum = tk.StringVar()
        self.kkm = tk.StringVar()
        self.scanfolder = tk.StringVar()
        
        # Add this printer dictionary
        self.center_printers = {
            'SFD': [
                'SFD-Drucker1',
                'SFD-Drucker2',
                'SFD-Office',
                'SFD-Empfang'
            ],
            'MLK': [
                'MLK-HP1',
                'MLK-Canon1',
                'MLK-Buero'
            ],
            'OOE': [
                'OOE-Hauptdrucker',
                'OOE-Empfang',
                'OOE-Schulung'
            ],
            'TRL': [
                'TRL-Drucker1',
                'TRL-Empfang',
                'TRL-Buero'
            ],
            'LEB': [
                'LEB-HP1',
                'LEB-Canon1',
                'LEB-Office'
            ],
            'KAL': [
                'KAL-Hauptdrucker',
                'KAL-Empfang',
                'KAL-Schulung'
            ],
            'KTN': [
                'KTN-Drucker1',
                'KTN-Empfang',
                'KTN-Buero'
            ],
            'TDF': [
                'TDF-HP-Office',
                'TDF-Canon-Empfang',
                'TDF-Schulungsraum',
                'TDF-Werkstatt'
            ]
        }
        
        # Style configuration
        style = ttk.Style()
        style.configure('TButton', padding=5)
        
        # Create main frame
        main_frame = ttk.Frame(root, padding="20")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Header
        header_frame = ttk.Frame(main_frame)
        header_frame.grid(row=0, column=0, columnspan=2, pady=(0, 20))
        ttk.Label(header_frame, text=f"Willkommen {os.getenv('USERNAME')}!", 
                 font=('Helvetica', 14, 'bold')).pack()
        ttk.Label(header_frame, text=f"PC-Name: {os.getenv('COMPUTERNAME')}", 
                 font=('Helvetica', 10)).pack()
        
        # Zentrum selection
        ttk.Label(main_frame, text="Zentrum auswählen:", 
                 font=('Helvetica', 10, 'bold')).grid(row=1, column=0, pady=5)
        self.zentrum_combo = ttk.Combobox(main_frame, 
                                   values=['SFD', 'MLK', 'OOE', 'TRL', 'LEB', 'KAL', 'KTN', 'TDF'],
                                   state='readonly')
        self.zentrum_combo.grid(row=1, column=1, pady=5)
        self.zentrum_combo.bind('<<ComboboxSelected>>', self.on_zentrum_select)
        
        # Create buttons frame
        buttons_frame = ttk.LabelFrame(main_frame, text="Verfügbare Aktionen", padding="20")
        buttons_frame.grid(row=2, column=0, columnspan=2, pady=20, sticky=(tk.W, tk.E))
        
        # Configure grid columns to be equal width
        buttons_frame.columnconfigure(0, weight=1)
        buttons_frame.columnconfigure(1, weight=1)
        
        # Add buttons with improved styling
        button_configs = [
            ("Drucker hinzufügen", self.add_printer),
            ("PDF-Drucker hinzufügen", self.add_pdf_printer),
            ("Vertriebsordner verknüpfen", self.setup_vertrieb),
            ("Scanordner verknüpfen", self.setup_scan),
            ("Desktop Links erstellen", self.create_desktop_links),
            ("KKM Verknüpfung", self.create_kkm_link),
            ("M:,N: Laufwerke verbinden", self.setup_shares),
            ("Zusätzlicher Zentrumsordner", self.add_zentrum_share)
        ]
        
        for idx, (text, command) in enumerate(button_configs):
            row = idx // 2
            col = idx % 2
            btn = ttk.Button(buttons_frame, text=text, command=command)
            btn.grid(row=row, column=col, pady=5, padx=5, sticky=(tk.W, tk.E))

    def on_zentrum_select(self, event):
        zentrum_map = {
            'SFD': ('3110', 'n3110', r'\\atlas\ftgroups\3110\Scan Dateien'),
            'MLK': ('3130', 'n3130', 'nicht_vorhanden'),
            'OOE': ('3140', 'n3140', r'\\atlas\ftgroups\3140\SCAN-Dateien'),
            'TRL': ('3160', 'n3160', r'\\atlas\ftgroups\3160\SCAN-Dateien'),
            'LEB': ('3180', 'n3180', r'\\atlas\ftgroups\3180\SCAN-Dateien'),
            'KAL': ('3280', 'n3280', 'nicht_vorhanden'),
            'KTN': ('3190', 'n3190', r'\\atlas\ftgroups\3190\Scan'),
            'TDF': ('3000', 'n3100', r'\\n3000\tt\Scan-Dateien')
        }
        
        selected = event.widget.get()
        if selected in zentrum_map:
            self.zentrum.set(zentrum_map[selected][0])
            self.kkm.set(zentrum_map[selected][1])
            self.scanfolder.set(zentrum_map[selected][2])

    def run_command(self, command, shell=True):
        try:
            result = subprocess.run(command, shell=shell, capture_output=True, text=True)
            if result.returncode != 0:
                messagebox.showerror("Fehler", f"Fehler bei der Ausführung:\n{result.stderr}")
                return False
            return True
        except Exception as e:
            messagebox.showerror("Fehler", f"Ein Fehler ist aufgetreten:\n{str(e)}")
            return False

    def add_printer(self):
        if not self.check_zentrum_selected():
            return
            
        selected_center = self.zentrum_combo.get()
        
        # Create a new top-level window
        printer_window = tk.Toplevel(self.root)
        printer_window.title(f"Drucker für {selected_center}")
        printer_window.geometry("400x300")
        
        # Create a frame for the printer list
        frame = ttk.Frame(printer_window, padding="20")
        frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Add a label
        ttk.Label(frame, text=f"Verfügbare Drucker in {selected_center}:", 
                 font=('Helvetica', 10, 'bold')).grid(row=0, column=0, pady=(0, 10))
        
        # Create a listbox with available printers
        printer_listbox = tk.Listbox(frame, selectmode=tk.MULTIPLE, width=40, height=10)
        printer_listbox.grid(row=1, column=0, pady=(0, 10))
        
        # Add scrollbar
        scrollbar = ttk.Scrollbar(frame, orient="vertical", command=printer_listbox.yview)
        scrollbar.grid(row=1, column=1, sticky=(tk.N, tk.S))
        printer_listbox.configure(yscrollcommand=scrollbar.set)
        
        # Insert printers for selected center
        for printer in self.center_printers[selected_center]:
            printer_listbox.insert(tk.END, printer)
        
        def install_selected_printers():
            selections = printer_listbox.curselection()
            if not selections:
                messagebox.showwarning("Warnung", "Bitte wählen Sie mindestens einen Drucker aus.")
                return
            
            server = f"n{self.zentrum.get()}"
            success_count = 0
            
            for index in selections:
                printer_name = printer_listbox.get(index)
                command = f'RUNDLL32 printui.dll,PrintUIEntry /in /n "\\\\{server}\\{printer_name}"'
                if self.run_command(command):
                    success_count += 1
            
            if success_count > 0:
                messagebox.showinfo("Erfolg", 
                                  f"{success_count} Drucker wurde(n) erfolgreich hinzugefügt.")
            printer_window.destroy()
        
        # Add install button
        ttk.Button(frame, text="Ausgewählte Drucker installieren", 
                   command=install_selected_printers).grid(row=2, column=0, pady=10)

    def add_pdf_printer(self):
        printers = ["pdf-mail", "pdf-mail-ft"]
        server = "pdfpr01"
        
        for printer in printers:
            command = f'RUNDLL32 printui.dll,PrintUIEntry /in /n "\\\\{server}\\{printer}"'
            self.run_command(command)
        
        messagebox.showinfo("Erfolg", "PDF-Drucker wurden hinzugefügt.")

    def setup_vertrieb(self):
        drive_letter = simpledialog.askstring("Laufwerk", "Laufwerksbuchstabe für Vertriebsordner (z.B. V:):")
        if drive_letter:
            if not drive_letter.endswith(':'): 
                drive_letter += ':'
            
            self.run_command(f'net use {drive_letter} /delete', shell=True)
            if self.run_command(f'net use {drive_letter} "\\\\n3000\\tt\\VERTRIEB  NFZ chg"'):
                messagebox.showinfo("Erfolg", f"Vertriebsordner wurde als {drive_letter} eingerichtet.")

    def setup_scan(self):
        if not self.check_zentrum_selected():
            return
            
        if self.scanfolder.get() == "nicht_vorhanden":
            messagebox.showinfo("Info", "Für dieses Zentrum gibt es keinen Scanordner.")
            return
            
        drive_letter = simpledialog.askstring("Laufwerk", "Laufwerksbuchstabe für Scanordner (z.B. S:):")
        if drive_letter:
            if not drive_letter.endswith(':'): 
                drive_letter += ':'
            
            self.run_command(f'net use {drive_letter} /delete')
            if self.run_command(f'net use {drive_letter} "{self.scanfolder.get()}"'):
                messagebox.showinfo("Erfolg", f"Scanordner wurde als {drive_letter} eingerichtet.")

    def create_desktop_links(self):
        desktop_path = str(Path.home() / "Desktop")
        
        # Create Outlook shortcut
        outlook_source = str(Path.home() / "AppData/Roaming/Microsoft/Windows/Start Menu/Programs/outlook.lnk")
        if os.path.exists(outlook_source):
            os.system(f'copy "{outlook_source}" "{desktop_path}"')
        
        # Create web shortcuts
        shortcuts = {
            "MeinCockpit.url": "https://lhrportal.oeamtc.at/Self/login",
            "CTOnline.url": "https://www.ctonline.at/auth",
            "BRZ_PortalAustria.url": "https://secure.portal.at/pat/#FSR"
        }
        
        for filename, url in shortcuts.items():
            shortcut_path = os.path.join(desktop_path, filename)
            with open(shortcut_path, 'w') as f:
                f.write(f"[InternetShortcut]\nURL={url}")
        
        messagebox.showinfo("Erfolg", "Desktop-Links wurden erstellt.")

    def setup_shares(self):
        if not self.check_zentrum_selected():
            return
            
        # Delete existing mappings
        self.run_command('net use M: /delete')
        self.run_command('net use N: /delete')
        
        if self.zentrum.get() == "3000":  # Teesdorf
            self.run_command(f'net use M: \\\\n3000\\users\\{os.getenv("USERNAME")}')
            self.run_command('net use N: \\\\n3000\\tt')
        else:  # Province
            self.run_command(f'net use M: \\\\atlas\\ftusers\\{os.getenv("USERNAME")}')
            self.run_command(f'net use N: \\\\atlas\\ftgroups\\{self.zentrum.get()}')
        
        messagebox.showinfo("Erfolg", "Netzwerklaufwerke M: und N: wurden eingerichtet.")

    def create_kkm_link(self):
        if not self.check_zentrum_selected():
            return
            
        rdp_path = os.path.join(str(Path.home()), "Desktop", "KKM.rdp")
        
        rdp_content = f"""screen mode id:i:2
use multimon:i:0
desktopwidth:i:1920
desktopheight:i:1080
session bpp:i:24
winposstr:s:0,1,922,-1080,2873,0
compression:i:1
keyboardhook:i:2
audiocapturemode:i:0
videoplaybackmode:i:1
connection type:i:7
networkautodetect:i:1
bandwidthautodetect:i:1
displayconnectionbar:i:1
enableworkspacereconnect:i:0
disable wallpaper:i:0
allow font smoothing:i:0
allow desktop composition:i:0
disable full window drag:i:1
disable menu anims:i:1
disable themes:i:0
disable cursor setting:i:0
bitmapcachepersistenable:i:1
full address:s:{self.kkm.get()}
audiomode:i:0
redirectprinters:i:1
redirectcomports:i:0
redirectsmartcards:i:1
redirectwebauthn:i:1
redirectclipboard:i:1
redirectposdevices:i:0
autoreconnection enabled:i:1
authentication level:i:2
prompt for credentials:i:0
negotiate security layer:i:1
remoteapplicationmode:i:0
alternate shell:s:
shell working directory:s:
gatewayhostname:s:
gatewayusagemethod:i:4
gatewaycredentialssource:i:4
gatewayprofileusagemethod:i:0
promptcredentialonce:i:0
gatewaybrokeringtype:i:0
use redirection server name:i:0
rdgiskdcproxy:i:0
kdcproxyname:s:
enablerdsaadauth:i:0
drivestoredirect:s:"""
        
        with open(rdp_path, 'w') as f:
            f.write(rdp_content)
        
        messagebox.showinfo("Erfolg", "KKM Verknüpfung wurde erstellt.")

    def add_zentrum_share(self):
        # Create a new top-level window
        share_window = tk.Toplevel(self.root)
        share_window.title("Zusätzliches Zentrum hinzufügen")
        share_window.geometry("400x200")
        
        frame = ttk.Frame(share_window, padding="20")
        frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Add a label for the dropdown
        ttk.Label(frame, text="Zentrum auswählen:", 
                 font=('Helvetica', 10, 'bold')).grid(row=0, column=0, pady=(0, 10))
        
        # Create the dropdown
        additional_zentrum = ttk.Combobox(frame, 
                                        values=['SFD', 'MLK', 'OOE', 'TRL', 'LEB', 'KAL', 'KTN', 'TDF'],
                                        state='readonly')
        additional_zentrum.grid(row=1, column=0, pady=(0, 20))
        
        def process_selection():
            selected_zentrum = additional_zentrum.get()
            if not selected_zentrum:
                messagebox.showwarning("Warnung", "Bitte wählen Sie ein Zentrum aus.")
                return
            
            # Mapping for the additional zentrum
            zentrum_map = {
                'SFD': '3110',
                'MLK': '3130',
                'OOE': '3140',
                'TRL': '3160',
                'LEB': '3180',
                'KAL': '3280',
                'KTN': '3190',
                'TDF': '3000'
            }
            
            # Ask for drive letter
            drive_letter = simpledialog.askstring("Laufwerk", 
                                                "Laufwerksbuchstabe für zusätzlichen Zentrumsordner (z.B. Z:):",
                                                parent=share_window)
            
            if drive_letter:
                if not drive_letter.endswith(':'): 
                    drive_letter += ':'
                
                self.run_command(f'net use {drive_letter} /delete')
                
                if zentrum_map[selected_zentrum] == "3000":
                    command = f'net use {drive_letter} \\\\n3000\\tt'
                else:
                    command = f'net use {drive_letter} \\\\atlas\\ftgroups\\{zentrum_map[selected_zentrum]}'
                
                if self.run_command(command):
                    messagebox.showinfo("Erfolg", 
                                      f"Zusätzlicher Zentrumsordner wurde als {drive_letter} eingerichtet.")
                    share_window.destroy()
        
        # Add confirm button
        ttk.Button(frame, text="Weiter", 
                   command=process_selection).grid(row=2, column=0, pady=10)

    def check_zentrum_selected(self):
        if not self.zentrum_combo.get():
            messagebox.showwarning("Warnung", "Bitte wählen Sie zuerst ein Zentrum aus.")
            return False
        return True

def main():
    root = tk.Tk()
    app = BuzeGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()