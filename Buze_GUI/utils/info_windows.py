import customtkinter as ctk # type: ignore

def create_help_window(parent):
    help_window = ctk.CTkToplevel(parent)
    help_window.title("Hilfe")
    help_window.geometry("600x400")
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
    1. Zentrum auswählen:
       - Wählen Sie zuerst Ihr Zentrum aus der Dropdown-Liste
    
    2. Drucker einrichten:
       - Klicken Sie auf 'Drucker hinzufügen'
       - Wählen Sie die gewünschten Drucker aus
    
    3. PDF-Drucker:
       - Der PDF-Drucker wird automatisch eingerichtet
    
    4. Netzlaufwerke:
       - M: und N: werden automatisch verbunden
       - Vertriebsordner kann separat eingebunden werden
    
    5. KKM-Verknüpfung:
       - Erstellt eine Verknüpfung zum KKM-System
       - Nur für lizenzierte PCs verfügbar
    
    Bei Problemen wenden Sie sich an den IT-Support.
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
    about_window.geometry("400x300")
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
    Dieses Tool wurde entwickelt, um die Einrichtung
    neuer Arbeitsplätze zu vereinfachen und zu
    standardisieren.
    
    © 2024 ÖAMTC Fahrtechnik
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