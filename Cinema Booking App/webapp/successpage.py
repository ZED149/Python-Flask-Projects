import sqlite3
import webbrowser

# importing libraries
from flask.views import MethodView
from flask import Flask, render_template, request, session, redirect, url_for
import os
import sqlite3
import json
from customer import Customer
from card import Card
from fpdf import FPDF
import yagmail

# global variables
p = os.path.abspath('databases')
BANKING_FILENAME = f"{p}/banking.db"
CINEMA_FILENAME = f"{p}/cinema.db"
path = os.path.abspath("webapp/")


class SuccessPage(MethodView):
    """

    """

    def post(self):
        seat_id = request.form.get("seat_id")
        # find price of seat
        seat_price = self.find_seat_price(seat_id)
        # need to validate form data with the DB
        return_string = self.check_card_details(request.form, cvc=request.form.get('cvc'),
                                                seat_price=seat_price)

        # creating pdf file
        customer = Customer(request.form.get('user_name'), request.form.get('user_email'))
        # extracting card balance from DB
        balance = self.extract_user_card_balance(request.form.get('cvc'))
        card = Card(request.form.get('holder_name'), request.form.get('card_type'),
                    request.form.get('card_number'), request.form.get('cvc'),
                    balance)
        total_amount = self.find_seat_price(seat_id)
        ticket = self.generate(customer, seat_id, total_amount)
        webbrowser.open(f'{(customer.name).title()}_ticket.pdf')
        # sending email to customer
        bill_file_name = os.path.abspath(f'{(customer.name).title()}_ticket.pdf')
        self.send_email(customer, bill_file_name)
        return redirect(url_for('home_page'))

    def check_card_details(self, req, cvc, seat_price):
        """
        This function checks data for card entered with the DB.
        :param seat_price:
        :param cvc:
        :param req:
        :return:
        """

        # first we need to make conn to db
        conn = sqlite3.connect(BANKING_FILENAME)
        cursor = conn.cursor()
        cursor.execute("""
        SELECT * FROM "Card" WHERE "cvc"=?
        """, [cvc])
        result = cursor.fetchall()
        if len(result) == 0:
            # it will execute if cvc is invalid
            obj = {
                "reponse":"card_details_invalid"
            }
            return json.dumps(obj)

        conn.close()
        if len(result) == 1:
            # it means we have found 1 record
            # now we need to validate that record with our form data
            checks = (request.form.get('holder_name'), request.form.get('card_number'),
                      request.form.get('card_type'))
            for _type, _number, _cvc, _holder_name, balance in result:
                if ((checks[2] == _type) and (checks[1] == _number) and
                        cvc == _cvc and
                        (checks[0] == _holder_name)) :
                    # check for balance
                    if balance >= seat_price:
                        # subtract user balance from database
                        obj = {
                            "reponse":"success"
                        }
                        json_format = json.dumps(obj)
                        return json_format
                    else:
                        obj = {
                            "response":"insufficient_balance"
                        }
                        return json.dumps(obj)
                else:
                    obj = {
                        "reponse":"card_details_invalid"
                    }
                    return json.dumps(obj)

    def find_seat_price(self, seat_id):
        conn = sqlite3.connect(CINEMA_FILENAME)
        cursor = conn.cursor()
        cursor.execute("""
        SELECT "price" FROM "Seat" WHERE "seat_id"=?
        """, [seat_id])
        result = cursor.fetchall()
        conn.close()
        return result[0][0]

    def extract_user_card_balance(self, cvc):
        """
        This function reads user card balance from DB.
        :param cvc:
        :return: balance
        """

        conn = sqlite3.connect(BANKING_FILENAME)
        cursor = conn.cursor()
        cursor.execute("""
        SELECT "balance" FROM "Card" WHERE "cvc"=?
        """, [cvc])
        result = cursor.fetchall()
        conn.close()
        balance = result[0][0]
        return balance

    def generate(self, customer, seat_id, total_amount):
        """
        This function generates a PDF document that contains
        the total bill amount its period
        and the distributed amount to be paid by the both flatmates
        :param customer:
        :param seat_id:
        :param total_amount:
        :return bill pdf object:
        """
        # creating an empty pdf document
        pdf = FPDF(orientation='P', unit='pt', format='A4')

        # adding an empty page to the document
        pdf.add_page()

        # now adding cells
        # adding an empty cell at the top
        pdf.set_font(family="Times", style='', size=0)

        # putting image
        webapp_path = os.path.abspath('webapp/')
        pdf.image(f"{webapp_path}/house.png", w=100, h=50)

        # setting font for title
        pdf.set_font(family="Times", style='BU', size=25)
        # putting Title
        pdf.cell(w=0, h=100, align='C', ln=1, txt="ZED Cinema Booking WebApp", border=1)

        # setting font for bill details
        pdf.set_font(family="Times", style='', size=15)
        # putting Customer details
        pdf.cell(w=150, h=50, txt="Name: ", align='C')
        pdf.cell(w=150, h=50, txt=str(customer.name), align='C', ln=1)
        pdf.cell(w=150, h=50, txt="Email: ", align='C')
        pdf.cell(w=150, h=50, txt=str(customer.email), ln=1, align='C')

        # putting end line
        pdf.cell(w=500, h=1, border=1, ln=1, align='C')

        # putting Bill details
        pdf.cell(w=150, h=50, txt="Seat ID: ", align='C')
        pdf.cell(w=150, h=50, txt=str(seat_id), align='C', ln=1)
        pdf.cell(w=150, h=50, txt="Amount: ", align='C')
        pdf.cell(w=150, h=50, txt=str(total_amount), ln=1, align='C')

        # putting end line
        pdf.cell(w=0, h=1, border=1, ln=1)

        # outputting
        pdf.output(f'{(customer.name).title()}_ticket.pdf')

    def send_email(self, customer, ticket):
        """
        This function sends an email containing ticket of the customer.
        :param customer:
        :param ticket:
        :return:
        """

        email = yagmail.SMTP("salmanahmad111499@gmail.com", "hozh uhdy dllv fpct")
        email.send(customer.email, subject=f"{(customer.name).capitalize()} your ZED Cinema Booking Ticket",
                   contents="Please find your ticket attached below. Thanks.",
                   attachments=ticket)
