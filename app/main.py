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
    t = [
        {"timestamp": "12-02-2020 10:20", "data": {"deaths": 1117, "confirmed": 45210, "recovered": 5133}},
        {"timestamp": "11-02-2020 10:00", "data": {"deaths": 1000, "confirmed": 44300, "recovered": 4700}},
        {"timestamp": "10-02-2020 10:00", "data": {"deaths": 800, "confirmed": 40000, "recovered": 4000}},
        {"timestamp": "09-02-2020 10:00", "data": {"deaths": 600, "confirmed": 30000, "recovered": 2500}},
        {"timestamp": "08-02-2020 10:00", "data": {"deaths": 300, "confirmed": 10000, "recovered": 1000}}
    ]
    return json.dumps(t)


@app.route('/api/by_country')
def api_by_country():
    d = dataStored.get_latest_value()
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
