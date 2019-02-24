
import numpy as np
from flask import Flask
from flask import request
from flask import send_from_directory
from flask import send_file
from flask import make_response

from trash_detector import process_image
from trash_detector import process_image_keras
from PIL import Image
from io import BytesIO
import cv2

app = Flask(__name__, static_url_path='')


@app.route('/')
def get_root():
    return send_from_directory('client', 'index.html')


@app.route('/static/<path:path>')
def get_static(path):
    return send_from_directory('client', path)


@app.route('/', methods=['POST'])
def post_root():
    data = request.files.get('input_image', '').read()
    nparr = np.frombuffer(data, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_ANYCOLOR)
    output = process_image(img)
    retval, buf = cv2.imencode('.png', output)
    response = make_response(buf.tobytes())
    response.headers['Content-Type'] = 'image/png'
    return response


@app.route('/keras', methods=['POST'])
def post_keras():
    data = request.files.get('input_image', '').read()
    nparr = np.frombuffer(data, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_ANYCOLOR)
    pil_img = Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
    output = process_image_keras(pil_img)
    img_io = BytesIO()
    output.save(img_io, 'PNG')
    img_io.seek(0)
    return send_file(img_io, mimetype='image/png')


if __name__ == '__main__':
    app.run(host='0.0.0.0',debug=True, port=3000)
