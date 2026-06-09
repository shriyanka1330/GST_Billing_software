import tkinter as tk
from tkinter import ttk, messagebox
from utils.base_form import BaseForm
from models.product import add_product, get_all_products

class ProductView:
    def __init__(self, parent):
        self.base = BaseForm(parent, "Product / Inventory Master")
        
        self.left_frame = tk.Frame(self.base.main, width=400)
        self.left_frame.pack(side="left", fill="y", padx=10, pady=10)
        
        self.right_frame = tk.Frame(self.base.main)
        self.right_frame.pack(side="left", fill="both", expand=True, padx=10, pady=10)

        self.setup_form()
        self.setup_table()
        self.load_data()

    def setup_form(self):
        tk.Label(self.left_frame, text="Product Name", font=("Arial", 10, "bold")).grid(row=0, column=0, pady=5, sticky="w")
        self.name_entry = tk.Entry(self.left_frame, width=30)
        self.name_entry.grid(row=0, column=1, pady=5)

        tk.Label(self.left_frame, text="Product Code", font=("Arial", 10, "bold")).grid(row=1, column=0, pady=5, sticky="w")
        self.code_entry = tk.Entry(self.left_frame, width=30)
        self.code_entry.grid(row=1, column=1, pady=5)

        tk.Label(self.left_frame, text="Price", font=("Arial", 10, "bold")).grid(row=2, column=0, pady=5, sticky="w")
        self.price_entry = tk.Entry(self.left_frame, width=30)
        self.price_entry.grid(row=2, column=1, pady=5)
        self.price_entry.insert(0, "0.00")

        tk.Label(self.left_frame, text="GST Rate (%)", font=("Arial", 10, "bold")).grid(row=3, column=0, pady=5, sticky="w")
        self.gst_cb = ttk.Combobox(self.left_frame, values=["0", "5", "12", "18", "28"], state="readonly", width=27)
        self.gst_cb.grid(row=3, column=1, pady=5)
        self.gst_cb.set("18")

        tk.Label(self.left_frame, text="Opening Stock", font=("Arial", 10, "bold")).grid(row=4, column=0, pady=5, sticky="w")
        self.stock_entry = tk.Entry(self.left_frame, width=30)
        self.stock_entry.grid(row=4, column=1, pady=5)
        self.stock_entry.insert(0, "0")

        tk.Button(self.left_frame, text="Save Product", bg="#4CAF50", fg="white", width=15, command=self.save_product).grid(row=5, column=1, pady=20, sticky="w")

    def setup_table(self):
        self.tree = ttk.Treeview(self.right_frame, columns=("ID", "Name", "Code", "Price", "GST", "Stock"), show="headings")
        self.tree.heading("ID", text="ID")
        self.tree.heading("Name", text="Product Name")
        self.tree.heading("Code", text="Product Code")
        self.tree.heading("Price", text="Price")
        self.tree.heading("GST", text="GST %")
        self.tree.heading("Stock", text="Stock")
        
        self.tree.column("ID", width=50)
        self.tree.column("Name", width=150)
        self.tree.column("Code", width=100)
        self.tree.column("Price", width=100)
        self.tree.column("GST", width=80)
        self.tree.column("Stock", width=80)
        
        self.tree.pack(fill="both", expand=True)

    def load_data(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        products = get_all_products()
        for p in products:
            self.tree.insert("", "end", values=(p['id'], p['name'], p['product_code'], p['price'], f"{p['gst_rate']}%", p['stock']))

    def save_product(self):
        name = self.name_entry.get().strip()
        code = self.code_entry.get().strip()
        price = self.price_entry.get().strip()
        gst = self.gst_cb.get()
        stock = self.stock_entry.get().strip()

        if not name:
            messagebox.showerror("Error", "Product Name is required")
            return
        
        try:
            price = float(price)
            gst = int(gst)
            stock = int(stock)
        except ValueError:
            messagebox.showerror("Error", "Price, GST, and Stock must be numbers")
            return

        try:
            add_product(name, code, price, gst, stock)
            messagebox.showinfo("Success", f"Product '{name}' saved successfully!")
            self.name_entry.delete(0, tk.END)
            self.code_entry.delete(0, tk.END)
            self.price_entry.delete(0, tk.END)
            self.price_entry.insert(0, "0.00")
            self.stock_entry.delete(0, tk.END)
            self.stock_entry.insert(0, "0")
            self.load_data()
        except Exception as e:
            messagebox.showerror("Database Error", str(e))