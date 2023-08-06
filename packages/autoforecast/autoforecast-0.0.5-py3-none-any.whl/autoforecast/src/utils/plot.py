import plotly.graph_objects as go
    
    y_train = (
        train_2016_.target.tolist() + train_2017_.target.tolist() 
        + train_2018_.target.tolist() + train_2019_.target.tolist()
    )
    x_2019 = list(map(str,range(201901, 201913)))

    fig = go.Figure(data=go.Scatter(x=x_2019, y=train_2019_['target'], name='2019'))
    fig.add_trace(go.Scatter(x=x_2019, y=train_2018_['target'], name='2018'))
    fig.add_trace(go.Scatter(x=x_2019, y=train_2017_['target'], name='2017'))
    fig.add_trace(go.Scatter(x=x_2019, y=train_2016_['target'], name='2016'))
    fig.add_trace(go.Scatter(x=x_2019, y=pred, name='pred'))
    title = (
        """" my title """"
        
    )
    print(title)
    fig.show()
