#!/usr/bin/python
# -*- coding: utf-8 -*-

from flask import Flask, render_template
from flask_bootstrap import Bootstrap
from data import DataModel
from timeloop import Timeloop
from datetime import timedelta
import json
import pygal

PULL_FROM_DATA = 10
REFRESH_BROWSER = 5

tl = Timeloop()

app = Flask(__name__)
Bootstrap(app)

global dataStored


@tl.job(interval=timedelta(seconds=PULL_FROM_DATA))
def fetch_data():
    dataStored.pull_data()


@app.route('/')
def index():
    return render_template('index.html', title='Coronavirus live feed', refresh_time=REFRESH_BROWSER)


@app.route('/overview')
def overview():
    statics = {'SARS':{'deaths'   :774,
                       'confirmed':8_098,
                       'recovered':7_324},
               'MERS':{'deaths'   :862,
                       'confirmed':2_506,
                       'recovered':1_644}}

    ncov = dataStored.get_latest_value()

    bar_plots = {}
    for category in statics['SARS'].keys():
        bar_plot = pygal.Bar()
        bar_plot.title = f'Total number of {category} as of {ncov["timestamp"]}'
        bar_plot.add('2019-nCov', ncov['data'][category])

        for static in statics.keys():
            bar_plot.add(static, statics[static][category])

        bar_plots[category+'_BAR'] = bar_plot.render_data_uri()

    return render_template('overview.html', title='Overview', **bar_plots)


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
