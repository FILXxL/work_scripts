import PyInstaller.__main__
import os

PyInstaller.__main__.run([
    'main.py',
    '--onefile',
    '--windowed',
    '--name=OEAMTC_Onboarding',
    '--icon=icon.ico',  # Optional: Add an icon file if you have one
    '--clean',
    '--add-data=README.txt;.'  # Optional: Add any additional files you want to include
])