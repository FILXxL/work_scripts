import PyInstaller.__main__

PyInstaller.__main__.run([
    'main.py',
    '--onefile',
    '--windowed',
    '--name=FT_Onboarding',
    '--icon=favicon.ico',  # Optional: Add an icon file if you have one
    '--clean',
])