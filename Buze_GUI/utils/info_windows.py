import customtkinter as ctk # type: ignore

def create_help_window(parent):
    help_window = ctk.CTkToplevel(parent)
    help_window.title("Hilfe")
    help_window.geometry("600x520")
    help_window.grab_set()  # Make window modal
    
    # Main frame with padding
    main_frame = ctk.CTkFrame(help_window)
    main_frame.pack(fill="both", expand=True, padx=20, pady=20)
    
    # Title
    ctk.CTkLabel(
        main_frame,
        text="Hilfe & Anleitung",
        font=ctk.CTkFont(size=20, weight="bold")
    ).pack(pady=(0, 20))
    
    # Create scrollable frame for content
    scroll_frame = ctk.CTkScrollableFrame(main_frame)
    scroll_frame.pack(fill="both", expand=True)
    
    help_text = """
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
    
    ctk.CTkLabel(
        scroll_frame,
        text=help_text,
        font=ctk.CTkFont(size=12),
        justify="left",
        wraplength=520
    ).pack(padx=10, pady=10)
    
    # Close button
    ctk.CTkButton(
        main_frame,
        text="Schließen",
        command=help_window.destroy,
        width=120,
        height=32
    ).pack(pady=(20, 0))

def create_about_window(parent):
    about_window = ctk.CTkToplevel(parent)
    about_window.title("Über")
    about_window.geometry("600x520")
    about_window.grab_set()  # Make window modal
    
    # Main frame with padding
    main_frame = ctk.CTkFrame(about_window)
    main_frame.pack(fill="both", expand=True, padx=20, pady=20)
    
    # Title
    ctk.CTkLabel(
        main_frame,
        text="ÖAMTC Fahrtechnik Onboarding",
        font=ctk.CTkFont(size=20, weight="bold")
    ).pack(pady=(0, 20))
    
    # Version info
    ctk.CTkLabel(
        main_frame,
        text="Version 1.0",
        font=ctk.CTkFont(size=14)
    ).pack(pady=(0, 20))
    
    # Description
    description = """
    Ein Tool zur automatischen Einrichtung von\n"
             "Arbeitsplätzen in der ÖAMTC Fahrtechnik.
             Dieses Programm automatisiert die Einrichtung von:
             • Netzwerkdruckern\n"
             "• Netzwerklaufwerken\n"
             "• Desktop-Verknüpfungen\n"
             "• Remote Desktop Verbindungen"
             Entwickelt von:\n"
             "IT-Abteilung\n"
             "ÖAMTC Fahrtechnik",
             
    
    
             Alle Rechte vorbehalten.\n\n
             "Build: 2024.01",
    
    © 2025 ÖAMTC Fahrtechnik
    """
    
    ctk.CTkLabel(
        main_frame,
        text=description,
        font=ctk.CTkFont(size=12),
        justify="center",
        wraplength=300
    ).pack(pady=20)
    
    # Close button
    ctk.CTkButton(
        main_frame,
        text="Schließen",
        command=about_window.destroy,
        width=120,
        height=32
    ).pack(pady=(20, 0)) 