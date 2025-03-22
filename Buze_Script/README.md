# ÖAMTC Fahrtechnik Setup Script

This script helps set up workstations for ÖAMTC Fahrtechnik centers. It provides a modular and maintainable structure for various setup tasks.

## Structure

```
Buze_Script/
├── config/
│   └── config.bat       # Global configuration and settings
├── lib/
│   ├── menu.bat         # Main menu and navigation
│   ├── network.bat      # Network drive mapping functions
│   ├── printers.bat     # Printer installation functions
│   └── shortcuts.bat    # Desktop shortcuts creation
└── main.bat             # Main entry point
```

## Features

1. Printer Setup
   - Add center-specific printers
   - Add PDF printers

2. Network Drive Mapping
   - Map Vertrieb folder
   - Map Scan folder
   - Map M: and N: drives
   - Map additional center folders

3. Desktop Shortcuts
   - Create Outlook shortcut
   - Create web shortcuts (Mein Cockpit, CT Online, BRZ Portal)
   - Create KKM RDP connection

## Usage

1. Run `main.bat`
2. Select your center using the center code (e.g., SFD, MLK, OOE, etc.)
3. Use the menu to perform desired setup tasks

## Center Codes

- SFD: Saalfelden (3110)
- MLK: Melk (3130)
- OOE: Oberösterreich (3140)
- TRL: Tirol (3160)
- LEB: Lebring (3180)
- KAL: Kalwang (3280)
- KTN: Kärnten (3190)
- TDF: Teesdorf (3000)

## Last Update

- Version: 2.0
- Date: 22.03.2024 