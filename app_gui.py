import tkinter as tk
from tkinter import messagebox
import qrcode
from datetime import datetime, timedelta
import csv
import os
import random
from twilio.rest import Client

# =====================
# Twilio Credentials
# =====================
TWILIO_ACCOUNT_SID = "AC1fad4058306d6c128abb5850f8a3c5e0"
TWILIO_AUTH_TOKEN = "cb8135fa128f715fd48337d874d5018e"
TWILIO_WHATSAPP = "whatsapp:+14155238886"   # Twilio sandbox WhatsApp number

client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

def generate_qr():
    visitor_name = entry_name.get()
    flat_number = entry_flat.get()
    contact_number = entry_contact.get()
    hours_valid = int(entry_hours.get())

    if not visitor_name or not flat_number or not contact_number:
        messagebox.showerror("Error", "Please fill all fields!")
        return

    # Step 1: Create unique tracking ID
    tracking_id = random.randint(100000, 999999)

    # Step 2: Generate expiry time
    expiry_time = datetime.now() + timedelta(hours=hours_valid)
    expiry_str = expiry_time.strftime("%Y-%m-%d %H:%M:%S")

    # Step 3: Prepare QR data (contains hidden tracking ID)
    data = f"""
Visitor Name: {visitor_name}
Flat Number: {flat_number}
Contact Number: {contact_number}
Tracking ID: {tracking_id}
Valid Until: {expiry_str}
"""
    # Step 4: Generate QR code
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=10,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{visitor_name.replace(' ', '_')}_{timestamp}.png"
    img.save(filename)

    # Step 5: Save visitor info into CSV
    csv_file = "visitors.csv"
    file_exists = os.path.isfile(csv_file)
    with open(csv_file, mode='a', newline='') as file:
        writer = csv.writer(file)
        if not file_exists:
            writer.writerow(["Name", "Flat Number", "Contact Number", "Tracking ID", "QR Filename", "Expiry Time"])
        writer.writerow([visitor_name, flat_number, contact_number, tracking_id, filename, expiry_str])

    # Step 6: Send WhatsApp message
    msg = f"""
Hello {visitor_name},

✅ Your Visitor QR Code has been generated.

🏠 Flat: {flat_number}  
📞 Contact: {contact_number}  
🔑 Tracking ID: {tracking_id}  
⏳ Valid Until: {expiry_str}  

Please show this QR at the gate.
"""

    try:
        client.messages.create(
            from_=TWILIO_WHATSAPP,
            body=msg,
            to=f"whatsapp:+91{contact_number}",  # sends to visitor's number
            media_url=["https://demo.twilio.com/owl.png"]  # placeholder image
        )
        messagebox.showinfo("Success", f"QR code saved as {filename} and sent via WhatsApp!\nTracking ID: {tracking_id}")
    except Exception as e:
        messagebox.showerror("Error", f"QR generated but WhatsApp sending failed: {e}")

# =====================
# GUI Setup
# =====================
root = tk.Tk()
root.title("Visitor QR Generator")

tk.Label(root, text="Visitor Name:").grid(row=0, column=0, padx=5, pady=5)
entry_name = tk.Entry(root)
entry_name.grid(row=0, column=1, padx=5, pady=5)

tk.Label(root, text="Flat Number:").grid(row=1, column=0, padx=5, pady=5)
entry_flat = tk.Entry(root)
entry_flat.grid(row=1, column=1, padx=5, pady=5)

tk.Label(root, text="Contact Number:").grid(row=2, column=0, padx=5, pady=5)
entry_contact = tk.Entry(root)
entry_contact.grid(row=2, column=1, padx=5, pady=5)

tk.Label(root, text="Valid For (Hours):").grid(row=3, column=0, padx=5, pady=5)
entry_hours = tk.Entry(root)
entry_hours.insert(0, "1")  # default 1 hour
entry_hours.grid(row=3, column=1, padx=5, pady=5)

btn_generate = tk.Button(root, text="Generate QR", command=generate_qr)
btn_generate.grid(row=4, column=0, columnspan=2, pady=10)

root.mainloop()
