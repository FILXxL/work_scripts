import customtkinter as ctk # type: ignore
from tkinter import messagebox, simpledialog
import os
from pathlib import Path
import sys
import psutil  # Add this import

from config.centers import CENTER_NAMES, ZENTRUM_MAP
from config.printers import CENTER_PRINTERS
from config.kkm_license import KKM_LICENSED_PCS
from utils.commands import run_command
from utils.gui_helpers import create_styled_window, create_frame, configure_styles
from utils.printer_window import create_printer_window
from utils.share_window import create_share_window
from utils.info_windows import create_help_window, create_about_window
from utils.shortcut_window import create_shortcut_window
from utils.custom_dialogs import CustomInputDialog

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

class BuzeGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("ÖAMTC Fahrtechnik Onboarding")
        self.root.geometry("900x620")
        
        # Set initial theme and color
        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme(resource_path("theme/yellow.json"))
        
        # Initialize variables
        self.zentrum = ctk.StringVar()
        self.kkm = ctk.StringVar()
        self.scanfolder = ctk.StringVar()
        
        # Configure root grid
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_rowconfigure(0, weight=1)
        
        # Setup GUI
        self.setup_gui()
    
    def setup_gui(self):
        # Create main frame
        main_frame = ctk.CTkFrame(self.root, fg_color=("gray95", "gray10"))  # Light mode color, Dark mode color
        main_frame.grid(row=0, column=0, padx=0, pady=0, sticky="nsew")  # Remove padding
        main_frame.grid_columnconfigure(0, weight=1)
        
        # Setup header
        self.setup_header(main_frame)
        
        # Setup center selection
        self.setup_center_selection(main_frame)
        
        # Setup action buttons
        self.setup_action_buttons(main_frame)
        
        # Add help and about buttons
        self.setup_info_buttons(main_frame)
        
        # Add appearance mode switch
        self.setup_appearance_switch(main_frame)
    
    def setup_header(self, main_frame):
        header_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        header_frame.grid(row=0, column=0, pady=(30, 30))  # Added top padding of 30
        
        ctk.CTkLabel(
            header_frame,
            text=f"Willkommen {os.getenv('USERNAME')}!",
            font=ctk.CTkFont(size=24, weight="bold")
        ).pack(pady=(0, 5))
        
        ctk.CTkLabel(
            header_frame,
            text=f"PC-Name: {os.getenv('COMPUTERNAME')}",
            font=ctk.CTkFont(size=14)
        ).pack()
    
    def setup_center_selection(self, main_frame):
        selection_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        selection_frame.grid(row=1, column=0, pady=(0, 20))
        selection_frame.grid_columnconfigure(1, weight=1)
        
        ctk.CTkLabel(
            selection_frame,
            text="Zentrum auswählen:",
            font=ctk.CTkFont(size=14, weight="bold")
        ).grid(row=0, column=0, padx=5)
        
        center_display_values = [f"{abbr} - {name}" for abbr, name in CENTER_NAMES.items()]
        self.zentrum_combo = ctk.CTkOptionMenu(
            selection_frame,
            values=center_display_values,
            command=self.on_zentrum_select,
            width=300
        )
        self.zentrum_combo.grid(row=0, column=1, padx=5)
    
    def setup_action_buttons(self, main_frame):
        buttons_frame = ctk.CTkFrame(main_frame)
        buttons_frame.grid(row=2, column=0, pady=20, sticky="ew")
        
        # Add title for the frame
        ctk.CTkLabel(
            buttons_frame,
            text="Verfügbare Aktionen",
            font=ctk.CTkFont(size=16, weight="bold")
        ).grid(row=0, column=0, columnspan=2, pady=(20, 30))  # Increased padding around title
        
        buttons_frame.grid_columnconfigure(0, weight=1)
        buttons_frame.grid_columnconfigure(1, weight=1)
        
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
            row = (idx // 2) + 1  # +1 because of title
            col = idx % 2
            btn = ctk.CTkButton(
                buttons_frame,
                text=text,
                command=command,
                width=300,
                height=35
            )
            btn.grid(row=row, column=col, pady=12, padx=20, sticky="ew")  # Increased button padding
    
    def setup_info_buttons(self, main_frame):
        info_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        info_frame.grid(row=4, column=0, pady=(20, 0), sticky="e")
        
        ctk.CTkButton(
            info_frame,
            text="Hilfe",
            command=lambda: create_help_window(self.root),
            width=120,
            height=32
        ).grid(row=0, column=0, padx=5)
        
        ctk.CTkButton(
            info_frame,
            text="Über",
            command=lambda: create_about_window(self.root),
            width=120,
            height=32
        ).grid(row=0, column=1, padx=5)
    
    def on_zentrum_select(self, choice):
        selected = choice[:3]
        if selected in ZENTRUM_MAP:
            self.zentrum.set(ZENTRUM_MAP[selected][0])
            self.kkm.set(ZENTRUM_MAP[selected][1])
            self.scanfolder.set(ZENTRUM_MAP[selected][2])
    
    def add_printer(self):
        if not self.check_zentrum_selected():
            return
        
        selected_center = self.zentrum_combo.get()[:3]
        selected_center_full = self.zentrum_combo.get()
        create_printer_window(self.root, selected_center, selected_center_full, 
                            CENTER_PRINTERS[selected_center], self.zentrum)
    
    def add_pdf_printer(self):
        printers = ["pdf-mail", "pdf-mail-ft"]
        server = "pdfpr01"
        
        for printer in printers:
            command = f'RUNDLL32 printui.dll,PrintUIEntry /in /n "\\\\{server}\\{printer}"'
            run_command(command)
        
        messagebox.showinfo("Erfolg", "PDF-Drucker wurden hinzugefügt.")
    
    def setup_vertrieb(self):
        dialog = CustomInputDialog(
            self.root,
            "Vertriebsordner verbinden",
            "Laufwerksbuchstabe (z.B. V:)"
        )
        
        drive_letter = dialog.result
        if drive_letter:
            run_command(f'net use {drive_letter} /delete', shell=True)
            if run_command(f'net use {drive_letter} "\\\\n3000\\tt\\VERTRIEB  NFZ chg"'):
                messagebox.showinfo("Erfolg", 
                                  f"Vertriebsordner wurde als {drive_letter} eingerichtet.")
    
    def setup_scan(self):
        if not self.check_zentrum_selected():
            return
        
        if self.scanfolder.get() == "nicht_vorhanden":
            messagebox.showinfo("Info", "Für dieses Zentrum gibt es keinen Scanordner.")
            return
        
        dialog = CustomInputDialog(
            self.root,
            "Scanordner verbinden",
            "Laufwerksbuchstabe (z.B. S:)"
        )
        
        drive_letter = dialog.result
        if drive_letter:
            run_command(f'net use {drive_letter} /delete')
            if run_command(f'net use {drive_letter} "{self.scanfolder.get()}"'):
                messagebox.showinfo("Erfolg", 
                                  f"Scanordner wurde als {drive_letter} eingerichtet.")
    
    def create_desktop_links(self):
        create_shortcut_window(self.root)
    
    def setup_shares(self):
        if not self.check_zentrum_selected():
            return
        
        run_command('net use M: /delete')
        run_command('net use N: /delete')
        
        if self.zentrum.get() == "3000":  # Teesdorf
            run_command(f'net use M: \\\\n3000\\users\\{os.getenv("USERNAME")}')
            run_command('net use N: \\\\n3000\\tt')
        else:  # Province
            run_command(f'net use M: \\\\atlas\\ftusers\\{os.getenv("USERNAME")}')
            run_command(f'net use N: \\\\atlas\\ftgroups\\{self.zentrum.get()}')
        
        messagebox.showinfo("Erfolg", "Netzwerklaufwerke M: und N: wurden eingerichtet.")
    
    def create_kkm_link(self):
        if not self.check_zentrum_selected():
            return
        
        current_pc = os.getenv('COMPUTERNAME')
        if current_pc not in KKM_LICENSED_PCS:
            response = messagebox.askyesno(
                "Achtung",
                "Dieser PC hat KEINE KKM Lizenz.\nMöchtest du trotzdem fortfahren?"
            )
            if not response:
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
        create_share_window(self.root, CENTER_NAMES)
    
    def check_zentrum_selected(self):
        if not self.zentrum_combo.get():
            messagebox.showwarning("Warnung", "Bitte wähle zuerst ein Zentrum aus.")
            return False
        return True

    def setup_appearance_switch(self, main_frame):
        switch_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        switch_frame.grid(row=4, column=0, pady=(20, 0), sticky="w")
        
        self.appearance_mode_switch = ctk.CTkSwitch(
            switch_frame,
            text="Dark Mode",
            command=self.change_appearance_mode,
            onvalue="dark",
            offvalue="light"
        )
        self.appearance_mode_switch.grid(row=0, column=0, padx=5)
        
        # Add uptime label
        self.uptime_label = ctk.CTkLabel(
            switch_frame,
            text=self.get_formatted_uptime(),
            font=ctk.CTkFont(size=12)
        )
        self.uptime_label.grid(row=1, column=0, padx=5, pady=(5, 0), sticky="w")
        
        # Update uptime every minute
        self.update_uptime()
        
        # Set initial switch state
        self.appearance_mode_switch.select() if ctk.get_appearance_mode() == "dark" else self.appearance_mode_switch.deselect()

    def update_uptime(self):
        self.uptime_label.configure(text=self.get_formatted_uptime())
        self.root.after(60000, self.update_uptime)  # Update every minute (60000 ms)

    def change_appearance_mode(self):
        new_mode = self.appearance_mode_switch.get()
        ctk.set_appearance_mode(new_mode)

    def get_formatted_uptime(self):
        uptime = psutil.boot_time()
        uptime_seconds = psutil.time.time() - uptime
        days = int(uptime_seconds // (24 * 3600))
        hours = int((uptime_seconds % (24 * 3600)) // 3600)
        minutes = int((uptime_seconds % 3600) // 60)
        return f"PC Uptime: {days}d {hours}h {minutes}m"

def main():
    root = ctk.CTk()
    app = BuzeGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()