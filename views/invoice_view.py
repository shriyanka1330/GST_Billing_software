import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
from utils.base_form import BaseForm
from models.ledger import get_all_ledgers
from models.product import get_all_products
from models.voucher import create_sales_voucher

class InvoiceView:
    def __init__(self, parent):
        self.base = BaseForm(parent, "Sales Voucher (Invoice)")

        self.products = get_all_products()
        self.ledgers = get_all_ledgers()
        
        # We only want Sundry Debtors or Cash for Sales usually, but we'll show all for simplicity
        self.ledger_map = {l['name']: l['id'] for l in self.ledgers}
        self.product_map = {p['name']: p for p in self.products}
        
        self.cart = []
        self.subtotal = 0
        self.cgst_total = 0
        self.sgst_total = 0
        self.igst_total = 0
        self.grand_total = 0

        # ===== 1. TOP FRAME =====
        top = tk.LabelFrame(self.base.main, text="Voucher Details", padx=10, pady=10)
        top.pack(fill="x", padx=10, pady=5)

        tk.Label(top, text="Date").grid(row=0, column=0, padx=5, pady=5)
        self.date_entry = tk.Entry(top)
        self.date_entry.grid(row=0, column=1)
        self.date_entry.insert(0, datetime.now().strftime("%Y-%m-%d"))

        tk.Label(top, text="Customer Name").grid(row=0, column=2, padx=10)
        self.ledger_cb = ttk.Combobox(top, values=list(self.ledger_map.keys()), state="readonly", width=30)
        self.ledger_cb.grid(row=0, column=3)
        
        # Intra-state vs Inter-state switch (For GST)
        tk.Label(top, text="Sale Type").grid(row=1, column=0, pady=5)
        self.sale_type_cb = ttk.Combobox(top, values=["Intra-State (CGST/SGST)", "Inter-State (IGST)"], state="readonly", width=25)
        self.sale_type_cb.grid(row=1, column=1)
        self.sale_type_cb.set("Intra-State (CGST/SGST)")

        # ===== 2. PRODUCT FRAME =====
        product = tk.LabelFrame(self.base.main, text="Add Item", padx=10, pady=10)
        product.pack(fill="x", padx=10, pady=5)

        tk.Label(product, text="Product").grid(row=0, column=0)
        self.product_cb = ttk.Combobox(product, values=list(self.product_map.keys()), state="readonly", width=25)
        self.product_cb.grid(row=0, column=1, padx=5)
        self.product_cb.bind("<<ComboboxSelected>>", self.on_product_select)

        tk.Label(product, text="Qty").grid(row=0, column=2)
        self.qty_entry = tk.Entry(product, width=10)
        self.qty_entry.grid(row=0, column=3, padx=5)

        tk.Label(product, text="Rate").grid(row=0, column=4)
        self.price_entry = tk.Entry(product, width=10)
        self.price_entry.grid(row=0, column=5, padx=5)

        tk.Label(product, text="GST %").grid(row=0, column=6)
        self.gst_entry = tk.Entry(product, width=10, state="readonly")
        self.gst_entry.grid(row=0, column=7, padx=5)

        tk.Button(product, text="Add Item", command=self.add_item, bg="#2196F3", fg="white").grid(row=0, column=8, padx=10)

        # ===== 3. TABLE =====
        table_frame = tk.Frame(self.base.main)
        table_frame.pack(fill="both", expand=True, padx=10, pady=5)

        self.table = ttk.Treeview(
            table_frame,
            columns=("Product", "Qty", "Rate", "GST %", "Tax Amt", "Total"),
            show="headings"
        )
        for col in ("Product", "Qty", "Rate", "GST %", "Tax Amt", "Total"):
            self.table.heading(col, text=col)
            self.table.column(col, width=100)
        self.table.pack(fill="both", expand=True)

        # ===== 4. TOTAL FRAME =====
        total_frame = tk.Frame(self.base.main)
        total_frame.pack(fill="x", padx=10, pady=5)

        self.lbl_subtotal = tk.Label(total_frame, text="Subtotal: 0.00", font=("Arial", 10))
        self.lbl_subtotal.pack(anchor="e")
        
        self.lbl_cgst = tk.Label(total_frame, text="CGST: 0.00", font=("Arial", 10))
        self.lbl_cgst.pack(anchor="e")
        
        self.lbl_sgst = tk.Label(total_frame, text="SGST: 0.00", font=("Arial", 10))
        self.lbl_sgst.pack(anchor="e")
        
        self.lbl_igst = tk.Label(total_frame, text="IGST: 0.00", font=("Arial", 10))
        self.lbl_igst.pack(anchor="e")
        
        self.lbl_grand = tk.Label(total_frame, text="Grand Total: 0.00", font=("Arial", 12, "bold"))
        self.lbl_grand.pack(anchor="e")

        # ===== 5. BUTTONS =====
        btn_f = tk.Frame(self.base.main)
        btn_f.pack(fill="x", padx=10, pady=10)
        tk.Button(btn_f, text="Save Voucher", command=self.save_voucher, bg="#4CAF50", fg="white", width=20).pack(side="right")

    def on_product_select(self, event=None):
        prod_name = self.product_cb.get()
        if prod_name in self.product_map:
            prod = self.product_map[prod_name]
            self.price_entry.delete(0, tk.END)
            self.price_entry.insert(0, str(prod['price']))
            
            self.gst_entry.config(state="normal")
            self.gst_entry.delete(0, tk.END)
            self.gst_entry.insert(0, str(prod['gst_rate']))
            self.gst_entry.config(state="readonly")

    def add_item(self):
        prod_name = self.product_cb.get()
        if not prod_name: return
        
        try:
            qty = int(self.qty_entry.get())
            price = float(self.price_entry.get())
            gst_rate = int(self.gst_entry.get())
        except:
            messagebox.showerror("Error", "Invalid Quantity or Price")
            return

        prod_id = self.product_map[prod_name]['id']
        subtotal = qty * price
        tax_amt = subtotal * (gst_rate / 100)
        total = subtotal + tax_amt

        item = {
            'product_id': prod_id,
            'name': prod_name,
            'quantity': qty,
            'price': price,
            'gst_rate': gst_rate,
            'tax_amt': tax_amt,
            'total': total
        }
        self.cart.append(item)
        
        self.table.insert("", "end", values=(prod_name, qty, price, gst_rate, round(tax_amt, 2), round(total, 2)))
        self.update_totals()

        # Clear
        self.qty_entry.delete(0, tk.END)

    def update_totals(self):
        self.subtotal = sum(i['price'] * i['quantity'] for i in self.cart)
        
        total_tax = sum(i['tax_amt'] for i in self.cart)
        
        sale_type = self.sale_type_cb.get()
        if "Intra-State" in sale_type:
            self.cgst_total = total_tax / 2
            self.sgst_total = total_tax / 2
            self.igst_total = 0
        else:
            self.cgst_total = 0
            self.sgst_total = 0
            self.igst_total = total_tax
            
        self.grand_total = self.subtotal + total_tax

        self.lbl_subtotal.config(text=f"Subtotal: {self.subtotal:.2f}")
        self.lbl_cgst.config(text=f"CGST: {self.cgst_total:.2f}")
        self.lbl_sgst.config(text=f"SGST: {self.sgst_total:.2f}")
        self.lbl_igst.config(text=f"IGST: {self.igst_total:.2f}")
        self.lbl_grand.config(text=f"Grand Total: {self.grand_total:.2f}")

    def save_voucher(self):
        ledger_name = self.ledger_cb.get()
        if not ledger_name:
            messagebox.showerror("Error", "Select a Customer Name")
            return
        if not self.cart:
            messagebox.showerror("Error", "Cart is empty")
            return

        ledger_id = self.ledger_map[ledger_name]
        date_str = self.date_entry.get()

        try:
            v_no = create_sales_voucher(
                date_str, 
                ledger_id, 
                self.cart, 
                self.subtotal, 
                self.cgst_total, 
                self.sgst_total, 
                self.igst_total, 
                self.grand_total
            )
            
            # GENERATE PDF
            try:
                from services.pdf_generator import generate_invoice_pdf
                
                # Fetch customer details for PDF
                customer = [l for l in self.ledgers if l['id'] == ledger_id][0]
                cust_gst = customer.get('gst_number', '')
                cust_addr = customer.get('address', '')
                
                pdf_path = generate_invoice_pdf(
                    voucher_no=v_no,
                    date=date_str,
                    customer_name=ledger_name,
                    customer_gst=cust_gst,
                    customer_address=cust_addr,
                    cart_items=self.cart,
                    subtotal=self.subtotal,
                    cgst=self.cgst_total,
                    sgst=self.sgst_total,
                    igst=self.igst_total,
                    grand_total=self.grand_total
                )
                
                resp = messagebox.askyesno("Success", f"Sales Voucher {v_no} generated successfully!\n\nDo you want to open the PDF Invoice?")
                if resp:
                    import os, platform
                    if platform.system() == 'Windows':
                        os.startfile(pdf_path)
                    elif platform.system() == 'Darwin':  # macOS
                        os.system(f"open '{pdf_path}'")
                    else:  # linux
                        os.system(f"xdg-open '{pdf_path}'")
                    
            except Exception as pdf_e:
                messagebox.showerror("PDF Error", f"Voucher saved, but PDF generation failed: {str(pdf_e)}")

            # Clear Form
            self.cart = []
            for item in self.table.get_children():
                self.table.delete(item)
            self.update_totals()
            self.ledger_cb.set('')
            
        except Exception as e:
            messagebox.showerror("Database Error", str(e))