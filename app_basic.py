import qrcode

print("Secure QR Visitor Management System starting...")

# Generate a QR code
data = "Welcome Visitor - Access Granted!"
qr = qrcode.QRCode(
    version=1,
    box_size=10,
    border=5
)
qr.add_data(data)
qr.make(fit=True)

# Save as image
img = qr.make_image(fill_color="black", back_color="white")
img.save("visitor_qr.png")

print("QR code generated and saved as visitor_qr.png ✅")



