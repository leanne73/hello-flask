import os
import sys
import time
import itertools
import numpy
from datetime import datetime
from datetime import timedelta
from flask import Flask, render_template, request, jsonify


class AppBrokenError(Exception):
    status_code = 500

    def __init__(self, message=None):
        self.message = message

    def to_dict(self):
        return {
            'message': self.message
        }

app = Flask(__name__)
broken_until = datetime.utcnow()

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/work', methods=['GET'])
def work():
    x = numpy.empty((3,3), dtype=int)
    for comb in itertools.product(range(10), repeat=9):
        x.flat[:] = comb
        try:
            inv = numpy.linalg.inv(x)
            print('inv calculated')
        except numpy.linalg.LinAlgError:
            # print('no inv')
            pass
    return render_template('index.html')

delay = os.environ.get('STARTUP_DELAY', None)
if delay:
    time.sleep(int(delay))

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=3838)
