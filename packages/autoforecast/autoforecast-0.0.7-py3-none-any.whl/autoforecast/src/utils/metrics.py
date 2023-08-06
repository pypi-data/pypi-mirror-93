import numpy as np
from sklearn.metrics import (
    mean_absolute_error, mean_absolute_percentage_error, mean_squared_error
)


def encode(data, col='bank'):
    map_col_to_col_id = {col: col_id for col_id, col in enumerate(data[col].unique())}
    data[f'{col}_token'] = data[col].map(map_col_to_col_id)
    return data, map_col_to_col_id


def smape_score(y_test, y_pred):
    """
    https://www.statology.org/smape-python/
    """
    y_test_ = []
    y_pred_ = []
    for test, pred in zip(y_test, y_pred):
        if abs(test) < 50 and abs(pred) < 50:
            y_test_.append(1)
            y_pred_.append(1)
        elif abs(test - pred) < 100:
            y_test_.append(1)
            y_pred_.append(1)
        else:
            y_test_.append(test)
            y_pred_.append(pred)

    y_test = np.array(y_test_)
    y_pred = np.array(y_pred_)
    if len(y_test) == 0:
        return 0.0
    return 1/len(y_test) * np.sum(2 * np.abs(y_pred-y_test) / (np.abs(y_test) + np.abs(y_pred))*100)


from sklearn.metrics import mean_absolute_percentage_error, mean_absolute_error, mean_squared_error


def get_metrics(y_pred, y_test, y_naive=None):
    mse = mean_squared_error(y_pred, y_test)
    rmse = np.sqrt(mse)
    rmsle = np.log(rmse)
    mape = mean_absolute_percentage_error(y_test, y_pred)
    mae = mean_absolute_error(y_true=y_test, y_pred=y_pred)
    y_pred = np.array(y_pred)
    y_test = np.array(y_test)
    # https://en.wikipedia.org/wiki/Symmetric_mean_absolute_percentage_error#
    smape = smape_score(y_pred, y_test)
    y_pred = np.array([0.0 if pred_ < 1e-6 else pred_ for pred_ in y_pred])
    mase = None
    if y_naive is not None:
        mae_naive = mean_absolute_error(y_true=y_test, y_pred=y_naive)
        if mae_naive == 0.0:
            if mae != 0.0:
                mae_naive = mae
            else:
                mase = 0.0
        mae_naive = mae if mae_naive == 0.0 else mae_naive
        if mase is None:
            mase = mae / mae_naive
    return {'mse': mse, 'rmse': rmse, 'rmsle': rmsle, 'mape': mape,
            'mae': mae, 'smape': smape, 'mase': mase}