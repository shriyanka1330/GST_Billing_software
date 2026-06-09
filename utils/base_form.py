import tkinter as tk

class BaseForm:
    def __init__(self, parent, title):
        self.main = tk.Frame(parent, bg="white")
        self.main.pack(fill="both", expand=True)

        # Header
        header = tk.Label(self.main, text=title,
                          bg="#8a8f00", fg="white",
                          font=("Arial", 16, "bold"),
                          pady=10)
        header.pack(fill="x")

        # Center form container
        self.form = tk.Frame(self.main, bd=2, relief="groove",
                             padx=30, pady=20)
        self.form.place(relx=0.5, rely=0.4, anchor="center")

        # Button area
        self.btn_frame = tk.Frame(self.main, bg="white")
        self.btn_frame.place(relx=0.5, rely=0.7, anchor="center")

    def add_buttons(self, submit_text="Submit"):
        tk.Button(self.btn_frame, text=submit_text, width=15).pack(side="left", padx=10)
        tk.Button(self.btn_frame, text="Clear", width=15).pack(side="left", padx=10)