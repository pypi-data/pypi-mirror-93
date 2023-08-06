# Auto Forecast
AutoML library for time series forecasting

## Getting started

Upgrade pip
```bash
$ pip install pip --upgrade
```

Install autoforecast
```bash
$ pip install autoforecast
```


### Run the example function
```python
from autoforecast.examples import autoforecast_bitcoin


res = autoforecast_bitcoin.run()
print(res)
```

### Use you own dataset
```python
from autoforecast.automl import AutoForecast

res_auto_forecast = AutoForecast(train).run_auto_forecast(
    X_train, y_train, X_test, y_test,
    verbose=False, max_time_in_sec=600
)
```
