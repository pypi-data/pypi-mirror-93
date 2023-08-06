from autoforecast.src.data.import_bitcoin_price import get_price_for_last_n_days
from autoforecast.src.models.models_baseline import BaselineMean
from autoforecast.src.utils.metrics import get_metrics

df_price = get_price_for_last_n_days(n=30, type='spot', currency_pair='BTC-USD')
print(df_price)

ind_cutoff = int(df_price.shape[0]* 0.8)
train = df_price[:ind_cutoff]
test = df_price[ind_cutoff:]

X_train = train['timestamp']
y_train = train.price
X_test = test['timestamp']
y_test = test.price

model = BaselineMean()
model.fit(X_train=X_train, y_train=y_train)

y_pred = model.predict(X_test=X_test)

metrics = get_metrics(y_test=y_test, y_pred=y_pred)
print(metrics)
