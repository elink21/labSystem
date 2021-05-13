from fpdf import FPDF
import os
import secrets as keys
from datetime import date
import qrcode
import pandas as pd


# measuring the space
width, height = 210, 297
margin = 20

# creating pdf file


def generateQR():
    # data for qr key code
    area = "Laboratorio de informatica"
    emissionDate = date.today().strftime("%d/%m/%Y")
    key = keys.token_urlsafe(32)
    qr = qrcode.make(area+","+emissionDate+","+key)
    qr.save('qr.png')
    return key


def printLogos(pdf):
    pdf.image("lab/static/img/logoLargo.png", 30, margin, (width - margin*3))


def printHeaders(pdf, initialDate,endDate,career):
    # Uaemex logo
    printLogos(pdf)

    title = f'Reporte generado el {date.today().strftime("%d/%m/%Y")}'

    pdf.ln(45)
    pdf.cell(margin)
    pdf.set_font(style="B", size=14)
    pdf.cell(width-margin*3, 0, title, 0, 0, 'C')

    pdf.set_font(size=12, style="I")

    pdf.ln(10)
    pdf.cell(margin)

    description = f"""Este documento contiene el reporte de prestamos realizados por  el laboratorio de electronica de la carrera de {career} dentro del periodo comprendido entre el {initialDate} al {endDate}."""
    if career=='all':
        description = f"""Este documento contiene el reporte de prestamos realizados por  el laboratorio de electronica dentro del periodo comprendido entre el {initialDate} al {endDate}."""

    pdf.multi_cell(w=width-margin*3, h=18, txt=description,
                   border=0, ln=0, align='J', max_line_height=6)


def printFooter(pdf, totalData, key):
    # QR code for validation and footer
    pdf.image("lab/static/img/customLogo.png", width-100, height-37, 80)
    pdf.image("qr.png", margin, height-38, 30)
    pdf.set_font('Arial', 'B', 8)
    pdf.text(52, height-30, txt='Clave de autenticidad:')
    pdf.text(52, height-25, txt=key[0:24])
    pdf.text(52, height-20, txt=key[24:])
    pages = totalData//18
    if totalData % 18:
        pages += 1
    pdf.text(52, height-16, txt=f'Pag. {pdf.page_no()} de {pages}')
    pdf.set_font('Arial', 'B', 12)

    pdf.text(52, height-11, "Laboratorios de informatica")

    pdf.set_font(size=12, style="I")


def printFile(data,initialDate, endDate,career):
    key = generateQR()

    pdf = FPDF()

    pdf.add_page()

    pdf.set_font('Arial', size=12)

    printHeaders(pdf,initialDate,endDate,career)

    headers = ['F. de prestamo', 'F. de retorno', 'Alumno', 'Equipo']
    printFooter(pdf, len(data), key)

    # Creating tables
    pdf.ln(10)
    col_width = width/5

    th = pdf.font_size

    # Printing headers
    pdf.set_font(size=12, style='B')
    less=8
    pdf.cell(margin-less)
    for h in headers:
        pdf.cell(col_width, 2*th, str(h), border=1)
    pdf.cell(margin-less)
    pdf.ln(2*th)

    pdf.set_font(size=8)

    for i in range(len(data)):
        row = data[i]
        if(i % 18 == 0 and i != 0):
            pdf.add_page()
            printLogos(pdf)
            printFooter(pdf, len(data), key)
            pdf.ln(50)
            pdf.set_font(size=12, style='B')
            pdf.cell(margin-less)
            for h in headers:
                pdf.cell(col_width, 2*th, str(h), border=1)
            pdf.cell(margin-less)
            pdf.ln(2*th)
        pdf.set_font(size=8)
        pdf.cell(margin-less)

        for datum in row:
            pdf.cell(col_width, 2*th, str(datum), border=1)
        pdf.cell(margin-less)
        pdf.ln(2*th)

    # save the pdf with name .pdf
    pdf.output(f'Reporte_de_uso.pdf')
