import os
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib import colors

COMPANY_NAME = "Zillionsoftech Company Pvt Ltd"
COMPANY_ADDRESS = "123 Tech Park, Innovation Hub, City - 400001"
COMPANY_GST = "27AAAAA0000A1Z5"

def generate_invoice_pdf(voucher_no, date, customer_name, customer_gst, customer_address, cart_items, subtotal, cgst, sgst, igst, grand_total):
    # Ensure directory exists using absolute path
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    invoices_dir = os.path.join(base_dir, "invoices")
    if not os.path.exists(invoices_dir):
        os.makedirs(invoices_dir)
        
    filename = os.path.join(invoices_dir, f"{voucher_no}.pdf")
        
    c = canvas.Canvas(filename, pagesize=A4)
    width, height = A4
    
    # 1. Header (Company Details)
    c.setFont("Helvetica-Bold", 18)
    c.drawString(50, height - 50, COMPANY_NAME)
    
    c.setFont("Helvetica", 10)
    c.drawString(50, height - 65, COMPANY_ADDRESS)
    c.drawString(50, height - 80, f"GSTIN: {COMPANY_GST}")
    
    # Title
    c.setFont("Helvetica-Bold", 14)
    c.drawCentredString(width / 2, height - 110, "TAX INVOICE")
    
    # Line
    c.line(50, height - 120, width - 50, height - 120)
    
    # 2. Invoice & Customer Details
    c.setFont("Helvetica-Bold", 10)
    c.drawString(50, height - 140, "Invoice No:")
    c.setFont("Helvetica", 10)
    c.drawString(120, height - 140, voucher_no)
    
    c.setFont("Helvetica-Bold", 10)
    c.drawString(50, height - 155, "Date:")
    c.setFont("Helvetica", 10)
    c.drawString(120, height - 155, date)
    
    # Customer Side
    c.setFont("Helvetica-Bold", 10)
    c.drawString(300, height - 140, "Billed To:")
    c.setFont("Helvetica", 10)
    c.drawString(300, height - 155, customer_name)
    if customer_address:
        c.drawString(300, height - 170, customer_address[:50]) # Truncate for safety
    if customer_gst:
        c.drawString(300, height - 185, f"GSTIN: {customer_gst}")
        
    # Line
    c.line(50, height - 200, width - 50, height - 200)
    
    # 3. Table Header
    y = height - 220
    c.setFont("Helvetica-Bold", 10)
    c.drawString(50, y, "Sl.")
    c.drawString(80, y, "Product Description")
    c.drawString(280, y, "Qty")
    c.drawString(330, y, "Rate")
    c.drawString(380, y, "GST %")
    c.drawString(430, y, "Tax Amt")
    c.drawString(490, y, "Total")
    
    c.line(50, y - 10, width - 50, y - 10)
    
    # 4. Table Rows
    y -= 25
    c.setFont("Helvetica", 10)
    for idx, item in enumerate(cart_items, start=1):
        c.drawString(50, y, str(idx))
        c.drawString(80, y, str(item['name'])[:35])
        c.drawString(280, y, str(item['quantity']))
        c.drawString(330, y, f"{item['price']:.2f}")
        c.drawString(380, y, f"{item['gst_rate']}%")
        c.drawString(430, y, f"{item['tax_amt']:.2f}")
        c.drawString(490, y, f"{item['total']:.2f}")
        y -= 20
        
        # Add new page if list is too long
        if y < 150:
            c.showPage()
            y = height - 50
    
    c.line(50, y, width - 50, y)
    
    # 5. Totals
    y -= 20
    c.setFont("Helvetica-Bold", 10)
    c.drawString(380, y, "Subtotal:")
    c.drawString(490, y, f"{subtotal:.2f}")
    
    if cgst > 0:
        y -= 20
        c.drawString(380, y, "CGST:")
        c.drawString(490, y, f"{cgst:.2f}")
        
    if sgst > 0:
        y -= 20
        c.drawString(380, y, "SGST:")
        c.drawString(490, y, f"{sgst:.2f}")
        
    if igst > 0:
        y -= 20
        c.drawString(380, y, "IGST:")
        c.drawString(490, y, f"{igst:.2f}")
        
    y -= 10
    c.line(380, y, width - 50, y)
    
    y -= 15
    c.setFont("Helvetica-Bold", 12)
    c.drawString(380, y, "Grand Total:")
    c.drawString(490, y, f"Rs. {grand_total:.2f}")
    
    # Footer
    c.setFont("Helvetica", 10)
    c.drawString(50, 100, "Terms & Conditions:")
    c.drawString(50, 85, "1. Goods once sold will not be taken back.")
    c.drawString(50, 70, "2. Subject to City Jurisdiction.")
    
    c.setFont("Helvetica-Bold", 10)
    c.drawString(400, 70, "Authorized Signatory")
    
    c.save()
    
    return filename