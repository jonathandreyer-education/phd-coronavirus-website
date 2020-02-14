# Small website to show real-time feed of Coronavirus (2019-nCov)

This website is based on data from [here](https://github.com/CSSEGISandData/COVID-19).

## Install dependencies
``` bash
pip install -r requirements.txt
```

## Running the code

By default, the back end will fetch data from the remote URL but it is possible to use local data time series.
``` bash
cd app/
python main.py
```

To use local data, create a folder _time_series_ inside the _app_ folder. Copy time series data (e.g. from [here](https://github.com/CSSEGISandData/COVID-19/tree/master/time_series)) into this new folder.
After that modify variable _USE_LOCAL_ to _True_ and after, run the application with those commands:
``` bash
cd app/
python main.py
```
