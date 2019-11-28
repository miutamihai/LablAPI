from flask import Flask, render_template, request

from functions.preprocess_input import preprocess_input
from functions.get_prediction import get_prediction
from functions.get_max_probability import get_max_probability

UPLOAD_FOLDER = '/static/uploads/'

PROCESSED_FOLDER = '/static/processed'

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])

app = Flask(__name__)


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
def home_page():
    return render_template('index.html')


@app.route('/upload', methods=['GET', 'POST'])
def upload_page():
    if request.method == 'POST':
        if 'file' not in request.files:
            return render_template('upload.html', msg='No file selected')
        file = request.files['file']
        if file.filename == '':
            return render_template('upload.html', msg='No file selected')

        if file and allowed_file(file.filename):
            processed_path = preprocess_input(file, app.instance_path)
            load = get_prediction(processed_path)
            result = get_max_probability(load)
            return render_template('upload.html',
                                   msg='Successfully processed',
                                   extracted_text=result)
    elif request.method == 'GET':
        return render_template('upload.html')


if __name__ == '__main__':
    app.run()
