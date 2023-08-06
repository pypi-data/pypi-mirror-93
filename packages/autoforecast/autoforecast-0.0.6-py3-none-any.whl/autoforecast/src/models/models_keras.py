# Forecasting/autoforecast/src/models/keras_models.py
import numpy as np
from keras import Model
from keras.layers import Dense, LSTM, Embedding, Input
from sklearn.preprocessing import MinMaxScaler
import tensorflow as tf


class BaseKeras():
    def __init__(self, train, n_input=12, n_features=1):
        self.scaler = MinMaxScaler()
        self.scaler.fit(train.target.values.reshape(-1, 1))
        train['target_scaled'] = self.scaler.transform(train.target.values.reshape(-1, 1))
        self.y_train = train['target_scaled'].values
        self.n_input = n_input
        self.n_features = 1
        self.X_train = np.array([self.y_train[i:i+self.n_input] for i in range(len(self.y_train)-self.n_input)])
        self.y_train = np.array([self.y_train[i+1:i+self.n_input+1] for i in range(len(self.y_train)-self.n_input)])

    def fit(self, *args):
        self.model = self.keras_model(self.n_input, self.n_features)
        self.model.fit(self.X_train, self.y_train, epochs=10, validation_split=0.1, verbose=0)

    def predict(self, *args):
        pred_list = self.predict_by_batch(
            self.model, self.X_train, self.n_input, self.n_features, self.scaler)
        return pred_list

    @staticmethod
    def keras_model(n_input, n_features, hidden_size_dense=3):
        inputs = Input(shape=(n_input, n_features))
        x = Dense(hidden_size_dense, activation='relu')(inputs)
        outputs = Dense(units=1)(x)
        model = Model(inputs=inputs, outputs=outputs)
        loss = tf.keras.losses.MeanAbsolutePercentageError()
        optimizer = tf.keras.optimizers.Adam()
        model.compile(
            loss=loss,
            optimizer=optimizer
        )
        return model

    @staticmethod
    def predict_by_batch(model, X_train, n_input, n_features, scaler):
        pred_list = []
        batch = X_train[-1].reshape(-1, 1)
        for i in range(n_input):  
            pred_list.append(model.predict(batch)[0]) 
            batch = np.append(batch[1:], pred_list[i].reshape(-1, 1), axis=0)
        pred_list = np.concatenate([i for i in pred_list]).reshape(-1, 1)
        return np.concatenate(scaler.inverse_transform(pred_list))


class LSTMKeras(BaseKeras):
    def __init__(self, train):
        return super().__init__(train=train)

    def fit(self, *args):
        return super().fit(*args)

    def predict(self, *args):
        return super().predict(*args)

    @staticmethod
    def keras_model(n_input, n_features, hidden_size_lstm=3):
        inputs = Input(shape=(n_input, n_features))
        x = LSTM(hidden_size_lstm, activation='relu')(inputs)
        outputs = Dense(units=1)(x)
        model = Model(inputs=inputs, outputs=outputs)
        loss = tf.keras.losses.MeanAbsolutePercentageError()
        optimizer = tf.keras.optimizers.Adam()
        model.compile(
            loss=loss,
            optimizer=optimizer
        )
        return model
