import tkinter as tk
from tkinter import ttk
from utils.base_form import BaseForm
from models.ledger import get_all_ledgers
from models.report import get_ledger_statement

class ReportView:
    def __init__(self, parent):
        self.base = BaseForm(parent, "Customer / Supplier Statement")
        
        self.ledgers = get_all_ledgers()
        self.ledger_map = {l['name']: l['id'] for l in self.ledgers}

        # TOP
        top = tk.Frame(self.base.main, pady=10)
        top.pack(fill="x")
        
        tk.Label(top, text="Select Name:", font=("Arial", 12, "bold")).pack(side="left", padx=10)
        self.ledger_cb = ttk.Combobox(top, values=list(self.ledger_map.keys()), state="readonly", width=30)
        self.ledger_cb.pack(side="left", padx=10)
        
        tk.Button(top, text="View Statement", command=self.load_report, bg="#2196F3", fg="white").pack(side="left", padx=10)

        # TABLE
        self.tree = ttk.Treeview(self.base.main, columns=("Date", "Voucher No", "Type", "Particulars", "Debit", "Credit", "Balance"), show="headings")
        self.tree.heading("Date", text="Date")
        self.tree.heading("Voucher No", text="Voucher No")
        self.tree.heading("Type", text="Vch Type")
        self.tree.heading("Particulars", text="Particulars")
        self.tree.heading("Debit", text="Debit (Dr)")
        self.tree.heading("Credit", text="Credit (Cr)")
        self.tree.heading("Balance", text="Balance")
        
        self.tree.pack(fill="both", expand=True, padx=10, pady=10)
        
        # BOTTOM SUMMARY
        bottom = tk.Frame(self.base.main, pady=10)
        bottom.pack(fill="x", padx=10)
        self.lbl_closing = tk.Label(bottom, text="Closing Balance: 0.00", font=("Arial", 14, "bold"))
        self.lbl_closing.pack(side="right")

    def load_report(self):
        lname = self.ledger_cb.get()
        if not lname: return
        
        for item in self.tree.get_children():
            self.tree.delete(item)
            
        l_id = self.ledger_map[lname]
        ledger, txns = get_ledger_statement(l_id)
        
        # Opening Balance Logic
        running_bal = float(ledger['opening_balance'])
        bal_type = ledger['balance_type']
        
        # Convert opening to a sign convention (Dr = +, Cr = -)
        if bal_type == 'Cr': running_bal = -running_bal
        
        self.tree.insert("", "end", values=("", "", "Opening Bal", "", 
                                            f"{ledger['opening_balance']}" if bal_type=='Dr' else "", 
                                            f"{ledger['opening_balance']}" if bal_type=='Cr' else "", 
                                            f"{abs(running_bal):.2f} {'Dr' if running_bal >= 0 else 'Cr'}"))
        
        for t in txns:
            dr_amt = t['amount'] if t['entry_type'] == 'Dr' else 0
            cr_amt = t['amount'] if t['entry_type'] == 'Cr' else 0
            
            running_bal += float(dr_amt)
            running_bal -= float(cr_amt)
            
            self.tree.insert("", "end", values=(
                t['date'], t['voucher_no'], t['voucher_type'], t['remarks'],
                dr_amt if dr_amt else "", cr_amt if cr_amt else "",
                f"{abs(running_bal):.2f} {'Dr' if running_bal >= 0 else 'Cr'}"
            ))
            
        self.lbl_closing.config(text=f"Closing Balance: {abs(running_bal):.2f} {'Dr' if running_bal >= 0 else 'Cr'}")
