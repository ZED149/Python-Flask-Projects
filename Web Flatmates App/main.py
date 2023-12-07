

# this is the main() for Web Flatmates App

# importing libraries
from bill import Bill
from flatmate import Flatmate
from pdf_report import PdfReport

# main()
# flatmates initialization
salman = Flatmate("Salman", 30)
awais = Flatmate("Awais", 50)

# bill initialization
bill = Bill(500, "November 2023")

# pdf initialization
pdf = PdfReport("files\\bill.pdf")
pdf.generate(salman, awais, bill)
