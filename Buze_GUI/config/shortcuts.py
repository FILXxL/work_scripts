from pathlib import Path

# Define the Outlook path once
OUTLOOK_PATH = str(Path.home() / "AppData/Roaming/Microsoft/Windows/Start Menu/Programs/outlook.lnk")

SHORTCUTS = {
    "MeinCockpit (LHR)": {
        "name": "MeinCockpit.url",
        "url": "https://lhrportal.oeamtc.at/Self/login"
    },
    "CTOnline": {
        "name": "CTOnline.url",
        "url": "https://www.ctonline.at/auth"
    },
    "BRZ Portal": {
        "name": "BRZ_PortalAustria.url",
        "url": "https://secure.portal.at/pat/#FSR"
    },
    "Outlook": {
        "name": "outlook.lnk",
        "type": "outlook_shortcut",
        "path": OUTLOOK_PATH
    }
} 