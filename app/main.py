#!/usr/bin/python
# -*- coding: utf-8 -*-

from flask import Flask, render_template
from flask_bootstrap import Bootstrap
from data import DataModel
from timeloop import Timeloop
from datetime import timedelta
import json

tl = Timeloop()

app = Flask(__name__)
Bootstrap(app)

global dataStored


@tl.job(interval=timedelta(seconds=10))
def fetch_data():
    dataStored.pull_data()


@app.route('/')
def index():
    return render_template('index.html', title='Coronavirus live feed')


@app.route('/api/latest')
def api_latest():
    d = dataStored.get_latest_value()
    return json.dumps(d)


@app.route('/api/timeseries')
def api_timeseries():
    d = dataStored.get_timeseries()
    return json.dumps(d)


@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_error(error):
    return render_template('500.html'), 500


if __name__ == '__main__':
    dataStored = DataModel()

    tl.start()

    app.run(host='0.0.0.0', port=5000, debug=True)

    tl.stop()
