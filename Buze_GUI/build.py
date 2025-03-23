from PyInstaller.__main__ import run # type: ignore

run([
    'main.py',
    '--onefile',
    '--windowed',
    '--name=FT_Onboarding',
    '--icon=favicon.ico',  # Optional: Add an icon file if you have one
    '--add-data=theme/yellow.json;theme',  # Simplified path without ./ and trailing slash
    '--debug=all',  # Add debug information
    '--clean',
])