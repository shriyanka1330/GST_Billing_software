import tkinter as tk
from tkinter import ttk, messagebox
from utils.base_form import BaseForm
from models.ledger import add_ledger, get_account_groups, get_all_ledgers

class LedgerView:
    def __init__(self, parent):
        self.base = BaseForm(parent, "Customer / Supplier Master")
        
        # Split main area into Left (Form) and Right (List)
        self.left_frame = tk.Frame(self.base.main, width=400)
        self.left_frame.pack(side="left", fill="y", padx=10, pady=10)
        
        self.right_frame = tk.Frame(self.base.main)
        self.right_frame.pack(side="left", fill="both", expand=True, padx=10, pady=10)

        self.setup_form()
        self.setup_table()
        self.load_data()

    def setup_form(self):
        # Fetch groups
        self.groups = get_account_groups()
        self.group_names = [g['name'] for g in self.groups]
        self.group_map = {g['name']: g['id'] for g in self.groups}

        tk.Label(self.left_frame, text="Name (Customer/Supplier)", font=("Arial", 10, "bold")).grid(row=0, column=0, pady=5, sticky="w")
        self.name_entry = tk.Entry(self.left_frame, width=30)
        self.name_entry.grid(row=0, column=1, pady=5)

        tk.Label(self.left_frame, text="Under Group", font=("Arial", 10, "bold")).grid(row=1, column=0, pady=5, sticky="w")
        self.group_cb = ttk.Combobox(self.left_frame, values=self.group_names, state="readonly", width=27)
        self.group_cb.grid(row=1, column=1, pady=5)
        if self.group_names:
            self.group_cb.set(self.group_names[0])

        tk.Label(self.left_frame, text="Opening Balance", font=("Arial", 10, "bold")).grid(row=2, column=0, pady=5, sticky="w")
        
        bal_frame = tk.Frame(self.left_frame)
        bal_frame.grid(row=2, column=1, pady=5, sticky="w")
        self.bal_entry = tk.Entry(bal_frame, width=15)
        self.bal_entry.pack(side="left")
        self.bal_entry.insert(0, "0.00")
        
        self.bal_type_cb = ttk.Combobox(bal_frame, values=["Dr", "Cr"], state="readonly", width=5)
        self.bal_type_cb.pack(side="left", padx=5)
        self.bal_type_cb.set("Dr")

        tk.Label(self.left_frame, text="GST Number", font=("Arial", 10, "bold")).grid(row=3, column=0, pady=5, sticky="w")
        self.gst_entry = tk.Entry(self.left_frame, width=30)
        self.gst_entry.grid(row=3, column=1, pady=5)

        tk.Label(self.left_frame, text="Address", font=("Arial", 10, "bold")).grid(row=4, column=0, pady=5, sticky="nw")
        self.address_text = tk.Text(self.left_frame, width=22, height=4)
        self.address_text.grid(row=4, column=1, pady=5)

        tk.Button(self.left_frame, text="Save Details", bg="#4CAF50", fg="white", width=15, command=self.save_ledger).grid(row=5, column=1, pady=20, sticky="w")

    def setup_table(self):
        self.tree = ttk.Treeview(self.right_frame, columns=("ID", "Name", "Group", "Balance"), show="headings")
        self.tree.heading("ID", text="ID")
        self.tree.heading("Name", text="Name")
        self.tree.heading("Group", text="Under Group")
        self.tree.heading("Balance", text="Opening Bal")
        
        self.tree.column("ID", width=50)
        self.tree.column("Name", width=150)
        self.tree.column("Group", width=150)
        self.tree.column("Balance", width=100)
        
        self.tree.pack(fill="both", expand=True)

    def load_data(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        ledgers = get_all_ledgers()
        for l in ledgers:
            bal_str = f"{l['opening_balance']} {l['balance_type']}"
            self.tree.insert("", "end", values=(l['id'], l['name'], l['group_name'], bal_str))

    def save_ledger(self):
        name = self.name_entry.get().strip()
        group_name = self.group_cb.get()
        bal = self.bal_entry.get().strip()
        bal_type = self.bal_type_cb.get()
        gst = self.gst_entry.get().strip()
        addr = self.address_text.get("1.0", tk.END).strip()

        if not name:
            messagebox.showerror("Error", "Name is required")
            return
        if not group_name:
            messagebox.showerror("Error", "Please select a group")
            return
        
        try:
            bal = float(bal)
        except ValueError:
            messagebox.showerror("Error", "Invalid Opening Balance")
            return

        group_id = self.group_map[group_name]

        try:
            add_ledger(name, group_id, bal, bal_type, gst, addr)
            messagebox.showinfo("Success", f"'{name}' saved successfully!")
            self.name_entry.delete(0, tk.END)
            self.bal_entry.delete(0, tk.END)
            self.bal_entry.insert(0, "0.00")
            self.gst_entry.delete(0, tk.END)
            self.address_text.delete("1.0", tk.END)
            self.load_data()
        except Exception as e:
            messagebox.showerror("Database Error", str(e))
