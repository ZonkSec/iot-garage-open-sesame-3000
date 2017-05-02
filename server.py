#!/usr/bin/python
import ssl
from flask import Flask, redirect, url_for, render_template_string, request
import gpiozero
from flask_wtf import FlaskForm
from wtforms import RadioField
from wtforms.validators import DataRequired

#GPIO Setup
leftGarage = gpiozero.DigitalOutputDevice(5)
rightGarage = gpiozero.DigitalOutputDevice(6)
rightGarage.off()
leftGarage.off()

#Flask Setup
app = Flask(__name__)
app.secret_key = 's3cr3t' #changeme

#Form Setup
class MyForm(FlaskForm):
        whichGarage = RadioField('Which garage?', choices=[('leftGarage','Left'),('rightGarage','Right')], validators=[DataRequired()])

#TLS Setup
CERT_FILE = '[mycert].cert'
KEY_FILE = '[mykey].key'
ssl_ctx = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
ssl_ctx.load_cert_chain(CERT_FILE, KEY_FILE)
ssl_ctx.verify_mode = ssl.CERT_REQUIRED
ssl_ctx.load_verify_locations(cafile=CERT_FILE)

#Main page Setup
@app.route('/',methods=['GET'])
def index():
    return render_template_string("""
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <html>
    <head><title>Open Sesame 3000</title></head>
    <body style="background-color:Black;color:Lime;">
        <pre>
   ____   ____   ______ _   __
  / __ \ / __ \ / ____// | / /
 / / / // /_/ // __/  /  |/ /
/ /_/ // ____// /___ / /|  /
\____//_/    /_____//_/ |_/

   _____  ______ _____  ___     __  ___ ______
  / ___/ / ____// ___/ /   |   /  |/  // ____/
  \__ \ / __/   \__ \ / /| |  / /|_/ // __/
 ___/ // /___  ___/ // ___ | / /  / // /___
/____//_____/ /____//_/  |_|/_/  /_//_____/

   _____  ____   ____   ____
  |__  / / __ \ / __ \ / __ \
   /_ < / / / // / / // / / /
 ___/ // /_/ // /_/ // /_/ /
/____/ \____/ \____/ \____/

  ad8888888888ba
 dP'         `"8b,
 8  ,aaa,       "Y888a     ,aaaa,     ,aaa,  ,aa,
 8  8' `8           "88baadP''''YbaaadP'''YbdP""Yb
 8  8   8              """        """      ""    8b
 8  8, ,8         ,aaaaaaaaaaaaaaaaaaaaaaaaddddd88P
 8  `''''       ,d8""
 Yb,         ,ad8"
  "Y8888888888P"

        </pre>
          <form method="POST" action="/garage">
                {{ form.csrf_token }}
                                {{ form.whichGarage.label }}
                                </br>
                                {% for subfield in form.whichGarage %}
                                        <table><td>
                                                <tr> {{ subfield }} </tr>
                                                <tr> {{ subfield.label }} </tr>
                                        </td></table>
                                {% endfor %}
                <input type="submit" value="Open!">
          </form>
    </body>
    </html>
    """,form=MyForm())

#garage page Setup
@app.route('/garage',methods=['POST'])
def led():
        garage = request.form.get('whichGarage')
        if garage == "rightGarage":
                print "opening right"
                rightGarage.blink(0.05,0.05,1)
        elif garage == "leftGarage":
                print "opening left"
                leftGarage.blink(0.05,0.05,2)
        return redirect(url_for('index'))

#Runs App
app.run('127.0.0.1', 443, app, ssl_context=ssl_ctx)
