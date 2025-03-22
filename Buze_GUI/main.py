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
        self.root.geometry("900x700")  # Slightly larger window
        
        # Variables - these need to be initialized before using them
        self.zentrum = tk.StringVar()
        self.kkm = tk.StringVar()
        self.scanfolder = tk.StringVar()
        
        # Configure root grid weights for centering
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_rowconfigure(0, weight=1)
        
        # Style configuration
        style = ttk.Style()
        style.configure('TButton', padding=10, font=('Helvetica', 10))
        style.configure('Header.TLabel', font=('Helvetica', 16, 'bold'), padding=10)
        style.configure('Subheader.TLabel', font=('Helvetica', 12), padding=5)
        style.configure('TLabelframe', padding=15)
        style.configure('TLabelframe.Label', font=('Helvetica', 11, 'bold'))
        
        # Create main frame with padding and configure its grid
        main_frame = ttk.Frame(root, padding="30")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        main_frame.grid_columnconfigure(0, weight=1)
        
        # Header - now centered
        header_frame = ttk.Frame(main_frame)
        header_frame.grid(row=0, column=0, pady=(0, 30))
        ttk.Label(header_frame, text=f"Willkommen {os.getenv('USERNAME')}!",
                 style='Header.TLabel').pack()
        ttk.Label(header_frame, text=f"PC-Name: {os.getenv('COMPUTERNAME')}",
                 style='Subheader.TLabel').pack()
        
        # Add this mapping for center names
        self.center_names = {
            'SFD': 'Saalfelden',
            'MLK': 'Melk',
            'OOE': 'Oberösterreich',
            'TRL': 'Tirol',
            'LEB': 'Lebring',
            'KAL': 'Kalwang',
            'KTN': 'Kärnten',
            'TDF': 'Teesdorf'
        }
        
        # Also need to add the printer dictionary back
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
        
        # Zentrum selection - centered
        selection_frame = ttk.Frame(main_frame)
        selection_frame.grid(row=1, column=0, pady=(0, 20))
        selection_frame.grid_columnconfigure(0, weight=1)
        selection_frame.grid_columnconfigure(1, weight=1)
        
        ttk.Label(selection_frame, text="Zentrum auswählen:",
                 font=('Helvetica', 11, 'bold')).grid(row=0, column=0, padx=5)
        
        # Create list of full names for dropdown
        center_display_values = [f"{abbr} - {name}" for abbr, name in self.center_names.items()]
        self.zentrum_combo = ttk.Combobox(selection_frame,
                                   values=center_display_values,
                                   state='readonly', width=30)
        self.zentrum_combo.grid(row=0, column=1, padx=5)
        self.zentrum_combo.bind('<<ComboboxSelected>>', self.on_zentrum_select)
        
        # Create buttons frame with improved styling
        buttons_frame = ttk.LabelFrame(main_frame, text="Verfügbare Aktionen", padding="25")
        buttons_frame.grid(row=2, column=0, pady=20, sticky=(tk.W, tk.E))
        
        # Configure grid for 2 columns of equal width
        buttons_frame.grid_columnconfigure(0, weight=1)
        buttons_frame.grid_columnconfigure(1, weight=1)
        
        # Add buttons with improved styling and spacing
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
            btn = ttk.Button(buttons_frame, text=text, command=command, width=30)
            btn.grid(row=row, column=col, pady=8, padx=10, sticky=(tk.W, tk.E))

    def on_zentrum_select(self, event):
        # Extract abbreviation from selection (first 3 characters)
        selected = event.widget.get()[:3]  # Gets 'SFD' from 'SFD - Saalfelden'
        
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
            
        selected_center = self.zentrum_combo.get()[:3]  # Get just the abbreviation (e.g., 'SFD' from 'SFD - Saalfelden')
        selected_center_full = self.zentrum_combo.get()  # Keep full name for display
        
        # Create a new top-level window
        printer_window = tk.Toplevel(self.root)
        printer_window.title(f"Drucker für {selected_center_full}")
        printer_window.geometry("400x300")
        
        # Create a frame for the printer list
        frame = ttk.Frame(printer_window, padding="20")
        frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Add a label
        ttk.Label(frame, text=f"Verfügbare Drucker in {selected_center_full}:", 
                 font=('Helvetica', 10, 'bold')).grid(row=0, column=0, pady=(0, 10))
        
        # Create a listbox with available printers
        printer_listbox = tk.Listbox(frame, selectmode=tk.MULTIPLE, width=40, height=10)
        printer_listbox.grid(row=1, column=0, pady=(0, 10))
        
        # Add scrollbar
        scrollbar = ttk.Scrollbar(frame, orient="vertical", command=printer_listbox.yview)
        scrollbar.grid(row=1, column=1, sticky=(tk.N, tk.S))
        printer_listbox.configure(yscrollcommand=scrollbar.set)
        
        # Insert printers for selected center using the abbreviation
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
        
        # Add install button with improved styling
        ttk.Button(frame, text="Ausgewählte Drucker installieren", 
                  command=install_selected_printers,
                  width=30).grid(row=2, column=0, pady=15)

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
        
        # Create list of full names for dropdown
        center_display_values = [f"{abbr} - {name}" for abbr, name in self.center_names.items()]
        
        # Create the dropdown
        additional_zentrum = ttk.Combobox(frame, 
                                        values=center_display_values,
                                        state='readonly')
        additional_zentrum.grid(row=1, column=0, pady=(0, 20))
        
        def process_selection():
            selected_zentrum = additional_zentrum.get()[:3]  # Gets abbreviation from selection
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