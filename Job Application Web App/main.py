
import sqlite3
import ssl
import smtplib
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from pathlib import Path

import pandas as pd
import numpy

# this is the main driver for Job Application webapp using flask

from flask import Flask, render_template, request

app = Flask(__name__)


def send_email(first_name, last_name, email, date, occupation):
    """
    Sends an email to the recipient of the form.
    :param first_name:
    :param last_name:
    :param email:
    :param date:
    :param occupation:
    :return:
    """

    host = "smtp.gmail.com"
    port = 465

    username = "salmanahmad111499@gmail.com"
    password = "hozh uhdy dllv fpct"

    receiver = email
    context = ssl.create_default_context()

    # creating pandas dataframe with column names
    df = pd.DataFrame(columns=['First Name', 'Last Name', 'Email', 'Date', 'Occupation'])

    # inserting columns values
    df.loc[len(df.index)] = [first_name, last_name, email, date, occupation]
    # writing to Excel file
    df.to_excel("info.xlsx", index=False)

    # message string
    message = (f"{first_name} {last_name} your job application form has been submitted successfully.\n"
               f"Details are attached below.")
    msg = MIMEMultipart()
    msg['From'] = username
    msg['To'] = receiver
    msg['Subject'] = 'Job Application Web App'

    msg.attach(MIMEText(message))

    path = Path('info.xlsx')
    part = MIMEBase('application', 'octet-stream')
    with open('info.xlsx', 'rb') as f:
        part.set_payload((f.read()))
    encoders.encode_base64(part)
    part.add_header('Content-Disposition', f'attachment; filename={Path(path).name}')
    msg.attach(part)

    with smtplib.SMTP_SSL(host, port, context=context) as server:
        server.login(username, password)
        server.sendmail(username, receiver, msg.as_string())


@app.route("/", methods=['GET', 'POST'])
def index():
    # checking request method
    if request.method == "POST":
        # extracting information from form
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        email = request.form['email']
        date = request.form['date']
        occupation = request.form['occupation']

        # connecting to database
        conn = sqlite3.connect('data.db')
        cursor = conn.cursor()
        # writing insert query
        query = """
        INSERT INTO person (first_name, last_name, email, date, occupation)
        VALUES (?, ?, ?, ?, ?)"""
        data_tuple = (first_name, last_name, email, date, occupation)
        conn.execute(query, data_tuple)
        conn.commit()
        conn.close()

        # sending email
        send_email(first_name, last_name, email, date, occupation)

        # rendering template
        return render_template("index.html", flag=True, first_name=first_name)

    else:
        return render_template("index.html", flag=False)


app.run(debug=True)


