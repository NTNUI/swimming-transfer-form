#! /usr/bin/python
import sys
import os
from PyPDF3 import PdfFileWriter, PdfFileReader
import io
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.utils import ImageReader
from reportlab.platypus import Image
import csv
from datetime import datetime

zip_codes_file = "zip-codes.txt"
transfer_form_file = "overgangsskjema2020.pdf"
association_transfer_file = "EndringAvKlubbtilhorighet2020.pdf"
signature_file = "signature.png"
signature_height = 20

# signature coordinates
transfer_signature_x = 142
transfer_signature_y = 670
association_signature_x = 142
association_signature_y = 589


def get_positions(x1_, y1_):
    # First group positions (Navn -> Ny klubb)
    x1 = x1_
    xp = x1 + 116  # zip position
    y1 = y1_
    dy1 = 28  # Distance between fields in first group

    # Checkmark position (gren)
    xc = x1+28
    yc = y1 - dy1*6 - 7

    # Second group positions (Sign)
    x2 = x1 + 40
    y2 = y1 - 228
    dy2 = 40

    return {
        "name": (x1, y1 - dy1*0),
        "birth_date": (x1, y1 - dy1*1),
        "address": (x1, y1 - dy1*2),
        "zip": (x1, y1 - dy1*3),
        "location": (xp, y1 - dy1*3),
        "licensee": (x1, y1 - dy1*4),
        "new": (x1, y1 - dy1*5),
        "X": (xc, yc),
        "date": (x2, y2 - dy2*0),
        "sign": (x2, y2 - dy2*1),
    }


def write_to_pdf(input_data, output_positions, templatefile, outputfile, signature=None):
    packet = io.BytesIO()
    # create a new PDF with Reportlab
    can = canvas.Canvas(packet, pagesize=A4)
    for entry in input_data:
        can.drawString(
            output_positions[entry][0], output_positions[entry][1], input_data[entry])
    if signature != None:
        iw, ih = signature.getSize()
        aspect = iw / float(ih)
        can.drawImage(signature, output_positions['sign'][0], output_positions['sign'][1],
                      width=(signature_height * aspect), height=signature_height)
    can.save()
    # move to the beginning of the StringIO buffer
    packet.seek(0)
    new_pdf = PdfFileReader(packet)
    # read your existing PDF
    existing_pdf = PdfFileReader(open(templatefile, "rb"))
    output = PdfFileWriter()
    # add the "watermark" (which is the new pdf) on the existing page
    page = existing_pdf.getPage(0)
    page.mergePage(new_pdf.getPage(0))
    output.addPage(page)
    # finally, write "output" to a real file
    outputStream = open(outputfile, "wb")
    output.write(outputStream)
    outputStream.close()

# use signature file
signature = None
if os.path.isfile(signature_file):
    signature = ImageReader(signature_file)

# read zip number and location from file
zip_locations = {}
with open(zip_codes_file, newline='', encoding="utf-8") as csvfile:
    reader = csv.reader(csvfile, delimiter='\t')
    for row in reader:
        zip_locations[int(row[0])] = row[1]

with open(sys.argv[1], newline='', encoding='utf8') as csvfile:
    output_positions = {}
    input_file = ""
    reader = csv.DictReader(csvfile, delimiter=',')
    for row in reader:
        data = {
            'name': row['first_name'] + " " + row['surname'],
            'birth_date': row['birth_date'],
            'address': row['address'],
            'licensee': row['licensee'],
            'new': "NTNUI-Svømming",
            'X': "X",
            'date': datetime.today().strftime('%d.%m.%y') + " - Trondheim",
        }
        try:
            data["zip"] = "{:04d}".format(int(row['zip']))
            data["location"] = zip_locations[int(row['zip'])]
        except KeyError:
            data["zip"] = "7030"
            data["location"] = "Trondheim"
        if (True): # set false for association transfer
            output_positions = get_positions(
                transfer_signature_x, transfer_signature_y)
            input_file = transfer_form_file
        else:
            output_positions = get_positions(
                association_signature_x, association_signature_y)
            input_file = association_transfer_file
        if not os.path.exists("output"):
            os.mkdir("output")
        write_to_pdf(data, output_positions, input_file,
                     "output/" + data['name'] + ".pdf", signature)
        print("Done " + data["name"])
