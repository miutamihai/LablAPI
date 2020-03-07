import json
import uuid
from functions.string_to_rgb import stringToRGB

import cv2
import numpy as np
import requests
from PIL import Image
from flask import Flask, render_template, request, url_for
from werkzeug.utils import redirect

from config import Config
from functions.get_max_probability import get_max_probability
from functions.get_prediction import get_prediction
from functions.preprocess_input import preprocess_input
from get_average_price import get_average_price
from validation import LoginForm

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
        print(file.filename)
        if file.filename == '':
            return 'File has no filename'
        if request.form['password'] != 'L@blAPI1268.!':
            return 'Access denied, wrong password'
        if file and allowed_file(file.filename):
            img = cv2.imdecode(np.fromstring(file.read(), np.uint8), cv2.IMREAD_COLOR)
            print('Successfully converted image')
            processed_path = preprocess_input(img)
            print('Successfully processed image')
            load = get_prediction(processed_path)
            print('Successfully got prediction')
            result = get_max_probability(load)
            if result == 'Unknown object':
                data = {'label': result, 'price': 'NA'}
                data = json.dumps(data)
                return data
            print(result)
            country = request.form['country']
            country = country[0].lower() + country[1:]
            print(country)
            data = {'label': result, 'price': get_average_price(result, country)}
            data = json.dumps(data)
            print(data)
            return data


@application.route('/get_average_price', methods=['POST'])
def get_average_price_route():
    if request.method == 'POST':
        label = request.form['label']
        country = request.form['country']
        data = {'label': label, 'price': get_average_price(label, country)}
        data = json.dumps(data)
        return data


@application.route('/binary', methods=['POST'])
def post_binary_file():
    if request.method == 'POST':
        print(type(request.form['image']))
        image = stringToRGB(request.form['image'])
        if request.form['password'] != 'L@blAPI1268.!':
            return 'Access denied, wrong password'
        else:
            processed_path = preprocess_input(image)
            load = get_prediction(processed_path)
            result = get_max_probability(load)
            country = request.form['country']
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
                country = 'Ireland'
                country = country[0].lower() + country[1:]
                # result = str(load)
                return render_template('upload.html',
                                       msg='Successfully processed',
                                       extracted_text=result + ' ' + get_average_price(result, country))
        elif request.method == 'GET':
            return render_template('upload.html')


if __name__ == '__main__':
    application.run(host='0.0.0.0')
