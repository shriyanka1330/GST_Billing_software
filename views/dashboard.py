import tkinter as tk
from PIL import Image, ImageTk  # pip install pillow

# Import views
# from views.customer_view import CustomerView
from views.invoice_view import InvoiceView

# Company Config (you can later move to DB)
COMPANY_NAME = "Zillionsoftech Company Pvt Ltd"
LOGO_PATH = "assets/logo.png"


class Dashboard:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Zillionsoftech GST Software")
        self.root.state("zoomed")

        # ===== MAIN CONTAINER =====
        container = tk.Frame(self.root)
        container.pack(fill="both", expand=True)

        # ===== SIDEBAR =====
        sidebar = tk.Frame(container, bg="#2c3e50", width=220)
        sidebar.pack(side="left", fill="y")

        tk.Label(sidebar,
                 text="GST SOFTWARE",
                 bg="#2c3e50",
                 fg="white",
                 font=("Arial", 16, "bold")).pack(pady=20)

        # Sidebar Buttons
        buttons = [
            ("Customer / Supplier", self.open_ledgers),
            ("Inventory (Products)", self.open_inventory),
            ("Sales Voucher", self.open_sales_voucher),
            ("Purchase Voucher", self.open_purchase),
            ("Payment/Receipt", self.open_payment),
            ("Reports", self.open_report),
            ("Logout", self.logout)
        ]

        for text, cmd in buttons:
            tk.Button(sidebar,
                      text=text,
                      width=20,
                      height=2,
                      command=cmd).pack(pady=5)

        # ===== RIGHT SIDE =====
        right_frame = tk.Frame(container, bg="white")
        right_frame.pack(side="left", fill="both", expand=True)

        # ===== HEADER =====
        self.header = tk.Frame(right_frame, bg="#ecf0f1", height=80)
        self.header.pack(fill="x")

        # Logo
        try:
            img = Image.open(LOGO_PATH)
            img = img.resize((60, 60))
            self.logo_img = ImageTk.PhotoImage(img)

            tk.Label(self.header,
                     image=self.logo_img,
                     bg="#ecf0f1").pack(side="left", padx=20)
        except:
            tk.Label(self.header,
                     text="[Logo]",
                     bg="#ecf0f1",
                     font=("Arial", 12)).pack(side="left", padx=20)

        # Company Name
        tk.Label(self.header,
                 text=COMPANY_NAME,
                 font=("Arial", 20, "bold"),
                 bg="#ecf0f1").pack(side="left")

        # Welcome Text
        self.page_title = tk.Label(self.header,
                                  text="Welcome Dashboard",
                                  font=("Arial", 16),
                                  bg="#ecf0f1")
        self.page_title.pack(side="right", padx=20)

        # ===== MAIN AREA =====
        self.main_area = tk.Frame(right_frame, bg="white")
        self.main_area.pack(fill="both", expand=True)

        # Default Screen
        # tk.Label(self.main_area,
        #          text="Welcome Dashboard",
        #          font=("Arial", 22),
        #          bg="white").pack(pady=50)

        self.root.mainloop()

    # ===== CLEAR MAIN AREA =====
    def clear_main(self):
        for widget in self.main_area.winfo_children():
            widget.destroy()

    # ===== BUTTON ACTIONS =====
    def open_ledgers(self):
        self.clear_main()
        self.page_title.config(text="Customer / Supplier Master")
        from views.ledger_view import LedgerView
        LedgerView(self.main_area)

    def open_inventory(self):
        self.clear_main()
        self.page_title.config(text="Product / Inventory Master")
        from views.product_view import ProductView
        ProductView(self.main_area)

    def open_sales_voucher(self):
        self.clear_main()
        self.page_title.config(text="Sales Voucher (Invoice)")
        InvoiceView(self.main_area)

    def open_purchase(self):
        self.clear_main()
        self.page_title.config(text="Purchase Voucher")
        from views.purchase_view import PurchaseView
        PurchaseView(self.main_area)

    def open_payment(self):
        self.clear_main()
        self.page_title.config(text="Payment / Receipt Voucher")
        from views.payment_view import PaymentView
        PaymentView(self.main_area)

    def open_report(self):
        self.clear_main()
        self.page_title.config(text="Ledger Statement / Reports")
        from views.report_view import ReportView
        ReportView(self.main_area)

    def logout(self):
        self.root.destroy()
        from views.login_view import LoginView
        LoginView().run()