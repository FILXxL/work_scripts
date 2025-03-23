import tkinter as tk
from tkinter import ttk

def center_window(window, width, height):
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x = (screen_width/2) - (width/2)
    y = (screen_height/2) - (height/2)
    window.geometry(f'{width}x{height}+{int(x)}+{int(y)}')

def create_help_window(parent):
    help_window = tk.Toplevel(parent)
    help_window.title("Hilfe")
    
    center_window(help_window, 800, 600)
    help_window.transient(parent)
    help_window.grab_set()
    
    # Main frame with weight configuration for centering
    frame = ttk.Frame(help_window, padding="30")
    frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
    help_window.grid_columnconfigure(0, weight=1)
    help_window.grid_rowconfigure(0, weight=1)
    frame.grid_columnconfigure(0, weight=1)
    
    # Centered title
    title_label = ttk.Label(frame, text="Hilfe & Anleitung",
                           font=('Helvetica', 16, 'bold'))
    title_label.grid(row=0, column=0, pady=(0, 20))
    
    # Text widget with centered content
    text_frame = ttk.Frame(frame)
    text_frame.grid(row=1, column=0, sticky=(tk.W, tk.E))
    text_frame.grid_columnconfigure(0, weight=1)
    
    help_text = tk.Text(text_frame, wrap=tk.WORD, width=70, height=25,
                       font=('Helvetica', 10))
    help_text.grid(row=0, column=0, pady=(0, 20))
    
    help_content = """
1. Zentrum auswählen
   - Wählen Sie Ihr Zentrum aus der Dropdown-Liste
   - Dies ist notwendig für die meisten weiteren Aktionen

2. Drucker einrichten
   - Klicken Sie auf "Drucker hinzufügen"
   - Wählen Sie die gewünschten Drucker aus der Liste
   - Mehrfachauswahl ist möglich
   - Die PDF-Drucker können separat hinzugefügt werden

3. Netzwerklaufwerke
   - "M:,N: Laufwerke verbinden" verbindet die Standardlaufwerke
   - M: ist Ihr persönlicher Ordner
   - N: ist der Zentrumsordner
   - Zusätzliche Laufwerke können über separate Optionen eingerichtet werden

4. Desktop-Links
   - Erstellt wichtige Verknüpfungen auf dem Desktop
   - Outlook (falls installiert)
   - MeinCockpit
   - CTOnline
   - BRZ Portal Austria

5. KKM Verknüpfung
   - Erstellt eine Remote Desktop Verbindung zum KKM
   - Die Verbindung wird auf dem Desktop gespeichert

6. Zusätzliche Funktionen
   - Vertriebsordner kann als separates Laufwerk eingebunden werden
   - Scanordner kann als separates Laufwerk eingebunden werden
   - Zusätzliche Zentrumsordner können eingebunden werden

Bei Problemen wenden Sie sich an:
IT-Support: +43 123 456789
E-Mail: support@example.com

Geschäftszeiten Support:
Montag - Donnerstag: 08:00 - 16:00
Freitag: 08:00 - 12:00
"""
    help_text.insert('1.0', help_content)
    help_text.config(state='disabled')
    
    # Center the text within the Text widget
    help_text.tag_configure('center', justify='center')
    help_text.tag_add('center', '1.0', 'end')
    
    # Scrollbar
    scrollbar = ttk.Scrollbar(text_frame, orient="vertical", command=help_text.yview)
    scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
    help_text.configure(yscrollcommand=scrollbar.set)
    
    # Centered close button
    button_frame = ttk.Frame(frame)
    button_frame.grid(row=2, column=0, pady=20)
    button_frame.grid_columnconfigure(0, weight=1)
    
    ttk.Button(button_frame, text="Schließen",
              command=help_window.destroy,
              width=20).grid(row=0, column=0)

def create_about_window(parent):
    about_window = tk.Toplevel(parent)
    about_window.title("Über")
    
    center_window(about_window, 500, 600)
    about_window.transient(parent)
    about_window.grab_set()
    
    # Main frame with weight configuration for centering
    frame = ttk.Frame(about_window, padding="30")
    frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
    about_window.grid_columnconfigure(0, weight=1)
    about_window.grid_rowconfigure(0, weight=1)
    frame.grid_columnconfigure(0, weight=1)
    
    # Centered title
    ttk.Label(frame, text="ÖAMTC Fahrtechnik Onboarding",
             font=('Helvetica', 16, 'bold'),
             justify='center').grid(row=0, column=0, pady=(0, 10))
    
    ttk.Label(frame, text="Version 1.0.0",
             font=('Helvetica', 12),
             justify='center').grid(row=1, column=0, pady=(0, 20))
    
    # About text with center alignment using multiple labels
    ttk.Label(frame, text="Ein Tool zur automatischen Einrichtung von\n"
             "Arbeitsplätzen in der ÖAMTC Fahrtechnik.",
             justify='center').grid(row=2, column=0, pady=(0, 20))
    
    ttk.Label(frame, text="Dieses Programm automatisiert die Einrichtung von:",
             justify='center').grid(row=3, column=0, pady=(0, 10))
    
    ttk.Label(frame, text="• Netzwerkdruckern\n"
             "• Netzwerklaufwerken\n"
             "• Desktop-Verknüpfungen\n"
             "• Remote Desktop Verbindungen",
             justify='center').grid(row=4, column=0, pady=(0, 20))
    
    ttk.Label(frame, text="Entwickelt von:\n"
             "IT-Abteilung\n"
             "ÖAMTC Fahrtechnik",
             justify='center').grid(row=5, column=0, pady=(0, 20))
    
    ttk.Label(frame, text="© 2024 ÖAMTC Fahrtechnik\n"
             "Alle Rechte vorbehalten.\n\n"
             "Build: 2024.01",
             justify='center').grid(row=6, column=0, pady=(0, 20))
    
    # Centered close button
    button_frame = ttk.Frame(frame)
    button_frame.grid(row=7, column=0, pady=10)
    button_frame.grid_columnconfigure(0, weight=1)
    
    ttk.Button(button_frame, text="Schließen",
              command=about_window.destroy,
              width=20).grid(row=0, column=0) 