
import numpy as np
from flask import Flask
from flask import request
from flask import send_from_directory
from flask import make_response

from trash_detector import process_image
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


if __name__ == '__main__':
    app.run(debug=True, port=3000)
