from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor, AdaBoostRegressor
from sklearn.linear_model import LinearRegression, Ridge, SGDRegressor
from sklearn.svm import LinearSVR, SVR, NuSVR
from sklearn.tree import DecisionTreeRegressor, ExtraTreeRegressor
from sklearn.neural_network import MLPRegressor
from sklearn.neighbors import KNeighborsRegressor
import xgboost as xgb

from src.models.models_keras import *
from src.models.models_baseline import *
from src.models.models_time_series import *


def get_dict_models(train):
    dict_models = {
        'LSTMKeras': LSTMKeras(train=train),
        'BaseKeras': BaseKeras(train=train),
        'XGBRegressor': xgb.XGBRegressor(),
        'RandomForestRegressor': RandomForestRegressor(),
        'GradientBoostingRegressor': GradientBoostingRegressor(),
        'AdaBoostRegressor': AdaBoostRegressor(),
        'LinearRegression': LinearRegression(),
        'Ridge': Ridge(),
        'SGDRegressor': SGDRegressor(),
        'LinearSVR': LinearSVR(),
        'SVR': SVR(),
        'NuSVR': NuSVR(),
        'DecisionTreeRegressor': DecisionTreeRegressor(),
        'ExtraTreeRegressor': ExtraTreeRegressor(),
        'MLPRegressor': MLPRegressor(),
        'KNeighborsRegressor': KNeighborsRegressor(),
        'ARMA': ARMA(),
        'BaselineLastYear': BaselineLastYear(),
        'BaselineLastValue': BaselineLastValue(),
        'BaselineMean': BaselineMean(),
        'BaselineMedian': BaselineMedian(),
        'Prophet': Prophet(train=train),
    }
    return dict_models
