# Forecasting/autoforecast/main.py
import numpy as np
import pandas as pd
import time
from tqdm import tqdm
import math

from autoforecast.src.utils.utils import *
from autoforecast.models.models import get_dict_models


class AutoForecast():
    def __init__(self, train, metrics=None):
        """
        metrics: str, metric to optimize
        """
        self.dict_models = get_dict_models(train)

    # custom AutoForecast
    def run_auto_forecast(
        self,
        X_train: np.ndarray,
        y_train: np.ndarray,
        X_test: np.ndarray,
        y_test: np.ndarray,
        verbose: bool = False,
        max_time_in_sec: int = 360
    ):
        """
        Args:
            :X_train: np.ndarray
            :y_train: np.ndarray
            :X_test: np.ndarray
            :y_test: np.ndarray
            :verbose: bool = False
            :max_time_in_sec: int = 360
        """
        print('AutoForecast starting...')
        start = time.time()
        dict_metrics = {}
        dict_pred = {}
        for model_str, model in tqdm(self.dict_models.items()):

            model = model
            model.fit(X_train, y_train)
            y_pred = model.predict(X_test)
            dict_pred[model_str] = y_pred
            if verbose:
                print(model_str)
                print(f'pred={y_pred}')
            metrics = get_metrics(y_test=y_test, y_pred=y_pred)
            dict_metrics[model_str] = metrics
            if start-time.time() >= max_time_in_sec:
                return {
                    'dict_metrics': dict_metrics,
                    'dict_pred': dict_pred
                }
        # print best models
        # RMSE
        print('Best models according to RMSE metrics:')
        dict_metrics_rmse = {k: v['rmse'] for k, v in dict_metrics.items()}
        # sorted dict
        dict_metrics_rmse = dict(sorted(dict_metrics_rmse.items(), key=lambda item: item[1]))
        print(dict_metrics_rmse)
        print('Best models according to MAPE metrics:')
        # MAPE
        dict_metrics_mape = {k: v['mape'] for k, v in dict_metrics.items()}
        # sorted dict
        dict_metrics_mape = dict(sorted(dict_metrics_mape.items(), key=lambda item: item[1]))
        print(dict_metrics_mape)
        print(f'AutoForecast done in {round(time.time()-start, 2)}s.')
        return {
            'dict_metrics': dict_metrics,
            'dict_pred': dict_pred
        }
