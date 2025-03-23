import tkinter as tk
from tkinter import ttk

def create_styled_window(title, geometry="400x300"):
    window = tk.Toplevel()
    window.title(title)
    window.geometry(geometry)
    return window

def create_frame(parent, padding="20"):
    frame = ttk.Frame(parent, padding=padding)
    frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
    return frame

def configure_styles(style):
    style.configure('TButton', padding=10, font=('Helvetica', 10))
    style.configure('Header.TLabel', font=('Helvetica', 16, 'bold'), padding=10)
    style.configure('Subheader.TLabel', font=('Helvetica', 12), padding=5)
    style.configure('TLabelframe', padding=15)
    style.configure('TLabelframe.Label', font=('Helvetica', 11, 'bold')) 