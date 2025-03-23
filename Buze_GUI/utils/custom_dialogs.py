import customtkinter as ctk # type: ignore

class CustomInputDialog:
    def __init__(self, parent, title, label_text):
        self.result = None
        
        # Create dialog window
        self.dialog = ctk.CTkToplevel(parent)
        self.dialog.title(title)
        self.dialog.geometry("400x200")
        self.dialog.grab_set()  # Make window modal
        
        # Center the window
        self.dialog.update_idletasks()
        screen_width = self.dialog.winfo_screenwidth()
        screen_height = self.dialog.winfo_screenheight()
        x = (screen_width - 400) // 2
        y = (screen_height - 200) // 2
        self.dialog.geometry(f"400x200+{x}+{y}")
        
        # Main frame with padding
        main_frame = ctk.CTkFrame(self.dialog)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Title
        ctk.CTkLabel(
            main_frame,
            text=title,
            font=ctk.CTkFont(size=16, weight="bold")
        ).pack(pady=(0, 20))
        
        # Input frame
        input_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        input_frame.pack(fill="x", pady=(0, 20))
        
        # Label
        ctk.CTkLabel(
            input_frame,
            text=label_text,
            font=ctk.CTkFont(size=12)
        ).pack(side="left", padx=(0, 10))
        
        # Entry
        self.entry = ctk.CTkEntry(input_frame, width=50)
        self.entry.pack(side="left")
        self.entry.insert(0, "")
        
        # Buttons frame
        button_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        button_frame.pack(fill="x", pady=(20, 0))
        
        # Cancel button
        ctk.CTkButton(
            button_frame,
            text="Abbrechen",
            command=self.cancel,
            width=120,
            height=32,
            fg_color="gray"
        ).pack(side="left", padx=5)
        
        # OK button
        ctk.CTkButton(
            button_frame,
            text="OK",
            command=self.ok,
            width=120,
            height=32
        ).pack(side="right", padx=5)
        
        # Wait for the dialog to be closed
        self.dialog.wait_window()
    
    def ok(self):
        self.result = self.entry.get()
        if not self.result.endswith(':'):
            self.result += ':'
        self.dialog.destroy()
    
    def cancel(self):
        self.dialog.destroy() 