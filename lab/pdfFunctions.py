from fpdf import FPDF
import os
import secrets as keys
from datetime import date
import qrcode
# creating pdf file


def generateQR():
    # data for qr key code
    area = "Laboratorio de electronica"
    emissionDate = date.today().strftime("%d/%m/%Y")
    key = keys.token_urlsafe(32)
    qr = qrcode.make(area+","+emissionDate+","+key)
    qr.save('qr.png')
    return key


key = generateQR()

pdf = FPDF()

pdf.add_page()

pdf.set_font('Arial', size=12)

# measuring the space
width, height = 210, 297
margin = 20

# Uaemex logo
pdf.image("lab/static/img/logoLargo.png", 30, margin, (width - margin*3))

pdf.ln(50)
pdf.cell(margin)
pdf.cell(width-margin*3, 10, 'Title', 1, 1, 'C')

# QR code for validation and footer
pdf.image("lab/static/img/customLogo.png", width-100, height-37, 80)
pdf.image("qr.png", margin, height-38, 30)
pdf.set_font('Arial','B',8)
pdf.text(52, height-30, txt='Clave de autenticidad:')
pdf.text(52, height-25, txt=key[0:24])
pdf.text(52, height-20, txt=key[24:])
pdf.set_font('Arial','B',12)
pdf.text(52, height-11, "Laboratorios de informatica")

# save the pdf with name .pdf
pdf.output("GFG.pdf")
