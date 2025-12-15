import qrcode
from datetime import datetime
import csv
import os

# Step 1: Get visitor input
visitor_name = input("Enter Visitor Name: ")
flat_number = input("Enter Flat Number: ")
contact_number = input("Enter Contact Number: ")

# Step 2: Prepare QR data
data = f"Visitor Name: {visitor_name}\nFlat Number: {flat_number}\nContact Number: {contact_number}"

# Step 3: Generate QR
qr = qrcode.QRCode(
    version=1,
    error_correction=qrcode.constants.ERROR_CORRECT_H,
    box_size=10,
    border=4,
)
qr.add_data(data)
qr.make(fit=True)
img = qr.make_image(fill_color="black", back_color="white")

# Step 4: Save QR with unique filename
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
filename = f"{visitor_name.replace(' ', '_')}_{timestamp}.png"
img.save(filename)

print(f"✅ QR code generated and saved as {filename}!")

# Step 5: Save visitor info in CSV
csv_file = "visitors.csv"
file_exists = os.path.isfile(csv_file)

with open(csv_file, mode='a', newline='') as file:
    writer = csv.writer(file)
    if not file_exists:
        writer.writerow(["Name", "Flat Number", "Contact Number", "QR Filename", "Timestamp"])
    writer.writerow([visitor_name, flat_number, contact_number, filename, timestamp])

print(f"✅ Visitor info saved in {csv_file}!")

# Step 6: Auto-open the QR (Mac only)
os.system(f"open {filename}")
