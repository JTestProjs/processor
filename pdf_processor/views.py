from django.shortcuts import render, redirect
from django.http import HttpResponse
import json
import os

from PyPDF2 import PdfFileWriter, PdfFileReader
import io
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont


def get_date(d: str, second_date: bool):
    year, month, day = d.split('-')
    months = {1: 'Jan', 2: 'Feb', 3: 'Mar', 4: 'Apr', 5: 'May', 6: 'Jun', 7: 'Jul', 8: 'Aug', 9: 'Sep', 10: 'Oct', 11: 'Nov', 12: 'Dec'}
    if second_date:
        m = int(month) + 3
        if m > 12:
            m = m - 12
            year = int(year) + 1
        month = months[m]
    else:
        month = months[int(month)]
    return '{} {}, {}'.format(month, int(day), year)

def processor(request): 

    d = request.POST['fromDate']

    first_date = get_date(d, False)
    second_date = get_date(d, True)

    packet = io.BytesIO()
    # create a new PDF with Reportlab
    can = canvas.Canvas(packet, pagesize=letter)
    can.setFont('Helvetica-Bold', 9.1)
    can.drawString(462, 122, "Smog Status:")
    can.setFont('Helvetica', 9.1)
    can.drawString(462, 105, "{} - {}".format(first_date, second_date))
    can.save()

    #move to the beginning of the StringIO buffer
    packet.seek(0)
    new_pdf = PdfFileReader(packet)
    # read your existing PDF
    existing_pdf = PdfFileReader(open("renewal_files/Calculate Vehicle Renewal Fees Results.pdf", "rb"))
    output = PdfFileWriter()
    # add the "watermark" (which is the new pdf) on the existing page
    page = existing_pdf.getPage(0)
    page.mergePage(new_pdf.getPage(0))
    output.addPage(page)
    # finally, write "output" to a real file
    outputStream = open("renewal_files/result.pdf", "wb")
    output.write(outputStream)
    outputStream.close()    
    return redirect('/')

def index(request):
    return render(request, 'pdf_processor/template.html', {})