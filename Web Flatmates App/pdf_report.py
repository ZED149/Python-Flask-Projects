

# this file contains the pdf_report class

# importing libraries
from fpdf import FPDF
import webbrowser

class PdfReport:
    """
    This class creates an object that can be used to generate a pdf document
    for flatmate and bill relation.
    """
    # constructor
    def __init__(self, filename):
        self.filename = filename

    # generate()
    def generate(self, flatmate1, flatmate2, bill):
        """
        This function generates a PDF document that contains
        the total bill amount its period
        and the distributed amount to be paid by the both flatmates
        :param flatmate1:
        :param flatmate2:
        :param bill:
        :return:
        """
        # creating an empty pdf document
        pdf = FPDF(orientation='P', unit='pt', format='A4')

        # adding an empty page to the document
        pdf.add_page()

        # now adding cells
        # adding an empty cell at the top
        pdf.set_font(family="Times", style='', size=0)

        # putting image
        pdf.image("files\\house.png", w=100, h=50)

        # setting font for title
        pdf.set_font(family="Times", style='BU', size=25)
        # putting Title
        pdf.cell(w=0, h=100, align='C', ln=1, txt="ZED FlatMate(s) Bill WebApp", border=1)

        # setting font for bill details
        pdf.set_font(family="Times", style='', size=15)
        # putting bill details
        pdf.cell(w=150, h=50, txt="Period: ", align='C')
        pdf.cell(w=150, h=50, txt=str(bill.period), align='C', ln=1)
        pdf.cell(w=150, h=50, txt="Amount: ", align='C')
        pdf.cell(w=150, h=50, txt=str(bill.amount), ln=1, align='C')

        # putting end line
        pdf.cell(w=0, h=1, border=1, ln=1)

        # putting flatmates details
        pdf.cell(w=150, h=50, align='C', txt=flatmate1.name)
        pdf.cell(w=150, h=50, align='C', txt=str(flatmate1.pays(bill, flatmate2)), ln=1)
        pdf.cell(w=150, h=50, align='C', txt=flatmate2.name)
        pdf.cell(w=150, h=50, align='C', txt=str(flatmate2.pays(bill, flatmate1)), ln=1)

        # putting end line
        pdf.cell(w=0, h=1, border=1, ln=1)

        # outputting
        pdf.output(self.filename)

        # opening in web browser
        webbrowser.open(self.filename)