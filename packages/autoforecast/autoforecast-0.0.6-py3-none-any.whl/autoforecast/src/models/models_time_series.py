# Forecasting/autoforecast/src/models/time_series_models.py
import numpy as np
import pandas as pd
import fbprophet
import statsmodels.api as sm


class ARMA():
    def __init__(self, order=None, period=None):
        self.order = order

    def fit(self, X_train, y_train):
        self.y_train = y_train
        aic_matrix = self.build_aic(
            y_train=self.y_train, p_max=6, q_max=6, p_min=0, q_min=0
        )
        self.order = self.best_order(aic_matrix)

    def predict(self, *arg):
        y_pred = self.predict_arma(y_train=self.y_train , order=self.order)
        return y_pred
    
    @staticmethod
    def build_aic(y_train: np.ndarray, p_max=6, q_max=6, p_min=0, q_min=0):
        aic_full = pd.DataFrame(np.zeros((6,6), dtype=float))
        # Iterate over all ARMA(p,q) models with p,q in [0,6]
        for p in range(6):
            for q in range(6):
                if p == 0 and q == 0:
                    continue
                # Estimate the model with no missing datapoints
                mod = sm.tsa.statespace.SARIMAX(y_train, order=(p,0,q), enforce_invertibility=False)
                try:
                    res = mod.fit(disp=False)
                    aic_full.iloc[p,q] = res.aic
                except:
                    aic_full.iloc[p,q] = np.nan
        return aic_full

    @staticmethod
    def best_order(aic_full: pd.DataFrame):
        aic_full.iloc[0,0]= 10.0**99
        # min column
        min_col_name = aic_full.min().idxmin()
        # min column index if needed
        min_col_idx = aic_full.columns.get_loc(min_col_name)
        # min row index
        min_row_idx = aic_full[min_col_name].idxmin()
        return (min_row_idx, 0, min_col_idx)

    @staticmethod
    def predict_arma(y_train: np.ndarray, order=(1, 0, 1)):
        mod = sm.tsa.statespace.SARIMAX(y_train, order=order)
        res = mod.fit(disp=False)
        # In-sample one-step-ahead predictions, and out-of-sample forecasts
        nforecast = 12
        predict = res.get_prediction(end=mod.nobs + nforecast)
        y_pred = predict.predicted_mean[-nforecast:]
        return np.array(y_pred)


class Prophet():
    def __init__(self, train, n_input=12):
        self.train = train
        self.model = None
        self.period = n_input

    def fit(self, X_train, y_train):
        if 'date' not in self.train.columns:
            raise "train df should have a 'date' column"
        df = pd.DataFrame({'ds': self.train.date, 'y': y_train})
        self.model = fbprophet.Prophet()
        self.model.fit(df)

    def predict(self, X_test):
        future = self.model.make_future_dataframe(periods=self.period, freq='M')
        forecast = self.model.predict(future)
        y_pred = forecast.yhat[-self.period:]
        return y_pred.values
