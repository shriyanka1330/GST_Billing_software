import tkinter as tk
from tkinter import messagebox
from controllers.auth_controller import login
from views.dashboard import Dashboard

class LoginView:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("GST Billing Software")

        # Fullscreen
        self.root.state("zoomed")   # Windows fullscreen

        # Main Frame (centered)
        frame = tk.Frame(self.root, bg="white", padx=40, pady=40)
        frame.place(relx=0.5, rely=0.5, anchor="center")

        tk.Label(frame, text="LOGIN", font=("Arial", 22, "bold"), bg="white").pack(pady=20)

        tk.Label(frame, text="Username", bg="white").pack(anchor="w")
        self.username = tk.Entry(frame, width=30)
        self.username.pack(pady=5)

        tk.Label(frame, text="Password", bg="white").pack(anchor="w")
        self.password = tk.Entry(frame, show="*", width=30)
        self.password.pack(pady=5)

        tk.Button(frame, text="Login", width=25, command=self.do_login, bg="#4CAF50", fg="white").pack(pady=20)

    def do_login(self):
        if login(self.username.get(), self.password.get()):
            self.root.destroy()
            Dashboard()
        else:
            messagebox.showerror("Error", "Invalid Username/Password")

    def run(self):
        self.root.mainloop()