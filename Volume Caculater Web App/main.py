

from flask import Flask, render_template, request


#  initializing our app
app = Flask(__name__)


# homepage
@app.route("/", methods=['GET', 'POST'])
def homepage():
    if request.method == "POST":
        # extracting values
        length = request.form['length']
        width = request.form['width']
        height = request.form['height']

        volume = float(length) * float(width) * float(height)

        return render_template('index.html', flag=True, volume=str(volume),
                               length=length, width=width, height=height, check="success")

    return render_template("index.html", flasg=False, check="warning")


# running our app
app.run(debug=True)
