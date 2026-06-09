import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
from utils.base_form import BaseForm
from models.ledger import get_all_ledgers
from models.voucher import create_payment_receipt_voucher

class PaymentView:
    def __init__(self, parent):
        self.base = BaseForm(parent, "Payment / Receipt Voucher")

        self.ledgers = get_all_ledgers()
        self.ledger_map = {l['name']: l['id'] for l in self.ledgers}

        # Main Frame
        frame = tk.Frame(self.base.main, padx=20, pady=20)
        frame.pack(fill="both", expand=True)

        # Voucher Type
        tk.Label(frame, text="Voucher Type", font=("Arial", 10, "bold")).grid(row=0, column=0, pady=10, sticky="w")
        self.vch_type_cb = ttk.Combobox(frame, values=["Payment", "Receipt"], state="readonly", width=30)
        self.vch_type_cb.grid(row=0, column=1, pady=10)
        self.vch_type_cb.set("Payment")
        self.vch_type_cb.bind("<<ComboboxSelected>>", self.on_type_change)

        # Date
        tk.Label(frame, text="Date", font=("Arial", 10, "bold")).grid(row=1, column=0, pady=10, sticky="w")
        self.date_entry = tk.Entry(frame, width=33)
        self.date_entry.grid(row=1, column=1, pady=10)
        self.date_entry.insert(0, datetime.now().strftime("%Y-%m-%d"))

        # Account (Cash/Bank) - Usually the Cr for Payment, Dr for Receipt
        self.lbl_ac = tk.Label(frame, text="Account (Cash/Bank)", font=("Arial", 10, "bold"))
        self.lbl_ac.grid(row=2, column=0, pady=10, sticky="w")
        self.ac_cb = ttk.Combobox(frame, values=list(self.ledger_map.keys()), state="readonly", width=30)
        self.ac_cb.grid(row=2, column=1, pady=10)

        # Particulars (Party) - Usually the Dr for Payment, Cr for Receipt
        self.lbl_part = tk.Label(frame, text="Customer / Supplier (Party)", font=("Arial", 10, "bold"))
        self.lbl_part.grid(row=3, column=0, pady=10, sticky="w")
        self.part_cb = ttk.Combobox(frame, values=list(self.ledger_map.keys()), state="readonly", width=30)
        self.part_cb.grid(row=3, column=1, pady=10)

        # Amount
        tk.Label(frame, text="Amount", font=("Arial", 10, "bold")).grid(row=4, column=0, pady=10, sticky="w")
        self.amt_entry = tk.Entry(frame, width=33)
        self.amt_entry.grid(row=4, column=1, pady=10)

        # Remarks
        tk.Label(frame, text="Remarks", font=("Arial", 10, "bold")).grid(row=5, column=0, pady=10, sticky="nw")
        self.remarks_text = tk.Text(frame, width=25, height=3)
        self.remarks_text.grid(row=5, column=1, pady=10)

        # Button
        tk.Button(frame, text="Save Voucher", command=self.save_voucher, bg="#4CAF50", fg="white", width=20).grid(row=6, column=1, pady=20, sticky="e")

        self.on_type_change()

    def on_type_change(self, event=None):
        v_type = self.vch_type_cb.get()
        if v_type == "Payment":
            # For Payment: Account is Credited (Cash goes out), Particulars is Debited
            self.lbl_ac.config(text="Account (Cash/Bank) [Cr]")
            self.lbl_part.config(text="Particulars (Party/Exp) [Dr]")
        else:
            # For Receipt: Account is Debited (Cash comes in), Particulars is Credited
            self.lbl_ac.config(text="Account (Cash/Bank) [Dr]")
            self.lbl_part.config(text="Particulars (Party/Inc) [Cr]")

    def save_voucher(self):
        v_type = self.vch_type_cb.get()
        date_str = self.date_entry.get().strip()
        ac_name = self.ac_cb.get()
        part_name = self.part_cb.get()
        amt_str = self.amt_entry.get().strip()
        remarks = self.remarks_text.get("1.0", tk.END).strip()

        if not ac_name or not part_name:
            messagebox.showerror("Error", "Please select both Account and Particulars.")
            return
            
        try:
            amount = float(amt_str)
            if amount <= 0: raise ValueError
        except ValueError:
            messagebox.showerror("Error", "Enter a valid positive amount.")
            return

        ac_id = self.ledger_map[ac_name]
        part_id = self.ledger_map[part_name]

        # Determine Dr and Cr based on voucher type
        if v_type == "Payment":
            dr_ledger_id = part_id
            cr_ledger_id = ac_id
        else:
            dr_ledger_id = ac_id
            cr_ledger_id = part_id

        try:
            v_no = create_payment_receipt_voucher(date_str, v_type, dr_ledger_id, cr_ledger_id, amount, remarks)
            messagebox.showinfo("Success", f"{v_type} Voucher {v_no} saved successfully!")
            
            # Clear form
            self.ac_cb.set('')
            self.part_cb.set('')
            self.amt_entry.delete(0, tk.END)
            self.remarks_text.delete("1.0", tk.END)
            
        except Exception as e:
            messagebox.showerror("Database Error", str(e))
