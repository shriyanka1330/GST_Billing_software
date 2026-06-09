def calculate_gst(amount, rate):
    gst = amount * rate / 100
    cgst = gst / 2
    sgst = gst / 2
    return cgst, sgst