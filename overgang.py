#! /usr/bin/python
####################################################################################
# Resurser tatt fra:
# "Postnummertabell Postnummer i rekkefølge Tab-separerte felter (ANSI)" fra
# https://www.bring.no/tjenester/adressetjenester/postnummer
#
# Skjema for overgang og endring av klubbtilhørighet fra
# https://svomming.no/forbundet/klubbdrift/organisasjon/overganger/
#
# csv-fil fra medlemsdatabasen (semi-kolon-separerte verdier), satt inn ekstra kolonner for:
# "gammelklubb" - tidligere klubb
# "overgang" - 'ja' om overgang kreves, 'nei' om endring av klubbtilhørighet holder
# Data hentet manuelt fra medley.no
#
# Alternativt: signatur.png - din egen signatur
#
#
# Use: python overgang.py <modifisert_medlemsdatabase.csv>
# Resulterende pdf-er havner i mappen "skjema"
####################################################################################
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

# Endre til å matche nye resurser
poststedfil = "Postnummerregister-ansi.txt"
overgangfil = "overgangsskjema2020.pdf"
endringfil = "EndringAvKlubbtilhorighet2020.pdf"
signaturfil = "signatur.png"
signaturheight = 20

# Posisjoner for feltene må kanskje endres hvis skjema endres
overgang_x = 142
overgang_y = 670
endring_x = 142
endring_y = 589


def get_positions(x1_, y1_):
    # First group positions (Navn -> Ny klubb)
    x1 = x1_
    xp = x1 + 116  # poststed position
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
        "birth": (x1, y1 - dy1*1),
        "addr": (x1, y1 - dy1*2),
        "post": (x1, y1 - dy1*3),
        "sted": (xp, y1 - dy1*3),
        "prev": (x1, y1 - dy1*4),
        "new": (x1, y1 - dy1*5),
        "X": (xc, yc),
        "date": (x2, y2 - dy2*0),
        "sign": (x2, y2 - dy2*1),
    }


test_data = {
    'name': "Ola Nordmann",
    'birth': "01.01.1970",
    'addr': "gate 123",
    'post': "0000",
    'sted': "Trondheim",
    'prev': "Gamleklubben",
    'new': "NTNUI-Svømming",
    'X': "X",
    'date': "01.01.2020 - Trondheim",
}


def write_to_pdf(input_data, output_positions, templatefile, outputfile, signatur=None):
    packet = io.BytesIO()
    # create a new PDF with Reportlab
    can = canvas.Canvas(packet, pagesize=A4)
    for entry in input_data:
        can.drawString(
            output_positions[entry][0], output_positions[entry][1], input_data[entry])
    if signatur != None:
        iw, ih = signatur.getSize()
        aspect = iw / float(ih)
        can.drawImage(signatur, output_positions['sign'][0], output_positions['sign'][1],
                      width=(signaturheight * aspect), height=signaturheight)
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


signatur = None
if os.path.isfile(signaturfil):
    signatur = ImageReader(signaturfil)

output_positions = get_positions(endring_x, endring_y)
write_to_pdf(test_data, output_positions, endringfil,
             test_data["name"]+".pdf", signatur)

poststeder = {}
with open(poststedfil, newline='', encoding="utf-8") as csvfile:
    reader = csv.reader(csvfile, delimiter='\t')
    for row in reader:
        poststeder[int(row[0])] = row[1]

with open(sys.argv[1], newline='', encoding='utf8') as csvfile:
    output_positions = {}
    inputfil = ""
    reader = csv.DictReader(csvfile, delimiter=';')
    for row in reader:
        print("building pdf for:")
        print(row)
        data = {
            'name': row['fornavn'] + " " + row['etternavn'],
            'birth': row['fodselsdato'],
            'addr': row['adresse'],
            'post': "{:04d}".format(int(row['postnr'])),
            'sted': poststeder[int(row['postnr'])],
            'prev': row['gammelklubb'],
            'new': "NTNUI-Svømming",
            'X': "X",
            # ta bort '#' for å legge til dato på signering
            'date': datetime.today().strftime('%d.%m.%y') + " - Trondheim",
        }
        print(data)
        if (row['overgang'] == 'ja'):
            output_positions = get_positions(overgang_x, overgang_y)
            inputfil = overgangfil
        else:
            output_positions = get_positions(endring_x, endring_y)
            inputfil = endringfil
        print("Using template " + inputfil)
        print("Writing to " + data['name'] + ".pdf")
        write_to_pdf(data, output_positions, inputfil,
                     "skjema/" + data['name'] + ".pdf", signatur)
        print("Done\n")
