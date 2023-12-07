

# this is the web representation of our app

# importing libraries
from flask.views import MethodView
from wtforms import Form, StringField, SubmitField
from flask import Flask, render_template, request

import flatmate
from bill import Bill
from flatmate import Flatmate
from pdf_report import PdfReport

app = Flask(__name__)

# Homepage class
class HomePage(MethodView):
    def get(self):
        return render_template("index.html")


# bill_form_page_class
class BillFormPage(MethodView):
    def get(self):
        bill_form = BillForm()
        return render_template("bill_form_page.html",
                               billform=bill_form)

    def post(self):
        bill_form = BillForm(request.form)
        bill = Bill(int(bill_form.amount.data), bill_form.period.data)
        flatmate1 = flatmate.Flatmate(bill_form.flatmate1.data, int(bill_form.days_in_house1.data))
        flatmate2 = flatmate.Flatmate(bill_form.flatmate2.data, int(bill_form.days_in_house2.data))
        # pdf initialization
        pdf = PdfReport("files\\bill.pdf")
        pdf.generate(flatmate1, flatmate2, bill)

        return render_template("bill_form_page.html",
                               name1=flatmate1.name, amount1=str(flatmate1.pays(bill, flatmate2)),
                               name2=flatmate2.name, amount2=str(flatmate2.pays(bill, flatmate1)),
                               billform=bill_form, result=True)

class ResultsPage(MethodView):
    pass

# bill form class
class BillForm(Form):
    amount = StringField("Bill amount: ", default=500)
    period = StringField("Time Period: ", default="November 2023")

    flatmate1 = StringField("Name1: ", default="Salman")
    flatmate2 = StringField("Name2: ", default="Awais")

    days_in_house1 = StringField("Days in house 1: ", default=30)
    days_in_house2 = StringField("Days in house 2: ", default=50)

    button = SubmitField("Calculate")


app.add_url_rule("/", view_func=HomePage.as_view("home_page"))
app.add_url_rule("/bill", view_func=BillFormPage.as_view("bill_form_page"))
# app.add_url_rule("/results", view_func=ResultsPage.as_view("results_page"))


app.run(debug=True)