#!/usr/bin/python

from datetime import datetime
from PyPDF3 import PdfFileWriter, PdfFileReader
from reportlab.lib.pagesizes import A4
from reportlab.lib.utils import ImageReader
from reportlab.pdfgen import canvas
import csv
import io
import os
import sys

zip_codes_file = "assets/zip-codes.txt"
transfer_form_file = "assets/overgangsskjema2022.pdf"
association_transfer_file = "assets/EndringAvKlubbtilhorighet2022.pdf"
signature_file = "assets/signature.png"

coords_transfer_pdf = {
    'name': (146, 624),
    'birth_date': (146, 596),
    'address': (146, 568),
    'zip': (146, 540),
    'location': (262, 540),
    'licensee': (146, 512),
    'new': (146, 484),
    'X': (170, 445),
    'date': (186, 386),
    'sign': (186, 346)
}

coords_association_pdf = {
    "name": (146, 569),
    "birth_date": (146, 541),
    "address": (146, 513),
    "zip": (146, 485),
    "location": (262, 485),
    "licensee": (146, 457),
    "new": (146, 429),
    "X": (170, 394),
    "date": (186, 341),
    "sign": (186, 301),
}


def write_to_pdf(input_data, output_positions, templatefile, outputfile, signature=None):
    packet = io.BytesIO()
    # create a new PDF with Reportlab
    can = canvas.Canvas(packet, pagesize=A4)
    # insert text into pdf
    for entry in input_data:
        can.drawString(
            output_positions[entry][0], output_positions[entry][1], input_data[entry])
    # insert signature into pdf
    if signature != None:
        iw, ih = signature.getSize()
        aspect = iw / float(ih)
        signature_height = 20
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


# read zip number and location from file
def get_zip_locations():
    zip_locations = {}
    with open(zip_codes_file, newline='', encoding="utf-8") as csvfile:
        reader = csv.reader(csvfile, delimiter='\t')
        for row in reader:
            zip_locations[int(row[0])] = row[1]
    return zip_locations

def main():
    with open(sys.argv[1], newline='', encoding='utf8') as csvfile:

        if not os.path.exists("output/transfer"):
            os.mkdir("output/transfer")
        if not os.path.exists("output/association"):
            os.mkdir("output/association")
        
        signature = None
        if os.path.isfile(signature_file):
            signature = ImageReader(signature_file)

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
                data["location"] = get_zip_locations()[int(row['zip'])]
            except KeyError:
                # Some internationals use their international zip location.
                # which will fail in the block above
                # Use some random Trondheim location as fallback
                data["zip"] = "7030"
                data["location"] = "Trondheim"


            write_to_pdf(data, coords_transfer_pdf, transfer_form_file,
                        "output/transfer/" + data['name'] + ".pdf", signature)
            write_to_pdf(data, coords_association_pdf, association_transfer_file,
                        "output/association/" + data['name'] + ".pdf", signature)
            print("Done ✅ " + data["name"])


if __name__ == "__main__":
    main()

