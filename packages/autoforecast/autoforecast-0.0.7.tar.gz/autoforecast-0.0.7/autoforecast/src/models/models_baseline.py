# Forecasting/autoforecast/src/models/baseline_models.py
import numpy as  np


class BaselineLastYear():
    def __init__(self, y_train=None):
        self.y_train = y_train

    def fit(self, X_train, y_train):
        self.y_train = y_train

    def predict(self, X_test):
        return np.array(self.y_train[-12:] * len(X_test))


class BaselineLastValue():
    def __init__(self, y_train=None):
        self.y_train = y_train

    def fit(self, X_train, y_train):
        self.y_train = y_train

    def predict(self, X_test):
        return np.array([self.y_train[-1]] * len(X_test))

    
class BaselineMean():
    def __init__(self, y_train=None):
        self.y_train = y_train

    def fit(self, X_train, y_train):
        self.y_train = y_train

    def predict(self, X_test):
        return np.array([np.mean(self.y_train)] * len(X_test))


class BaselineMedian():
    def __init__(self, y_train=None):
        self.y_train = y_train

    def fit(self, X_train, y_train):
        self.y_train = y_train

    def predict(self, X_test):
        return np.array([np.median(self.y_train)] * len(X_test))
