import uuid
import json

import requests
import cv2
import numpy as np
from flask import Flask, render_template, request, url_for
from werkzeug.utils import redirect

from config import Config
from functions.get_max_probability import get_max_probability
from functions.get_prediction import get_prediction
from functions.preprocess_input import preprocess_input
from validation import LoginForm
from get_average_price import get_average_price

UPLOAD_FOLDER = '/static/uploads/'

PROCESSED_FOLDER = '/static/processed'

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])

ACCESS_KEY = uuid.uuid1()

application = Flask(__name__)
application.config.from_object(Config)


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@application.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.password.data != 'L@blAPI1268.!':
            return 'password not correct'
        else:
            global ACCESS_KEY
            ACCESS_KEY = uuid.uuid1()
            return redirect(url_for('upload_page', access_key=ACCESS_KEY))
    return render_template('login.html', title='Sign In', form=form)


@application.route('/', methods=['POST'])
def home_page():
    if request.method == 'POST':
        if 'file' not in request.files:
            return 'No file found'
        file = request.files['file']
        if file.filename == '':
            return 'No file found'
        if request.form['password'] != 'L@blAPI1268.!':
            return 'Access denied, wrong password'
        if file and allowed_file(file.filename):
            img = cv2.imdecode(np.fromstring(file.read(), np.uint8), cv2.IMREAD_COLOR)
            processed_path = preprocess_input(img)
            load = get_prediction(processed_path)
            result = get_max_probability(load)
            country = request.country['country']
            country = country[0].lower() + country[1:]
            data = {'label': result, 'price': get_average_price(result, country)}
            data = json.dumps(data)
            return data


@application.route('/upload/<uuid:access_key>', methods=['GET', 'POST'])
def upload_page(access_key):
    if access_key != ACCESS_KEY:
        return 'Access denied'
    else:
        if request.method == 'POST':
            if 'file' not in request.files:
                return render_template('upload.html', msg='No file selected')
            file = request.files['file']
            if file.filename == '':
                return render_template('upload.html', msg='No file selected')
            if file and allowed_file(file.filename):
                img = cv2.imdecode(np.fromstring(file.read(), np.uint8), cv2.IMREAD_COLOR)
                processed_path = preprocess_input(img)
                load = get_prediction(processed_path)
                result = get_max_probability(load)
                r = requests.get('https://api.ipdata.co?api-key=test').json()
                country = r['country_name']
                country = country[0].lower() + country[1:]
                # result = str(load)
                return render_template('upload.html',
                                       msg='Successfully processed',
                                       extracted_text=result + ' ' + get_average_price(result, country))
        elif request.method == 'GET':
            return render_template('upload.html')


if __name__ == '__main__':
    application.run(host='0.0.0.0')
