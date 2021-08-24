# -*- coding: utf-8 -*-
"""Neev_Covid_Forecasting.ipynb
Automatically generated by Colaboratory.
Original file is located at
    https://colab.research.google.com/drive/1NyFTWPxMg3otN5mWZH6Eqz3H0G65DSVg
"""

import pandas as pd
import statsmodels 
from datetime import datetime
from datetime import timedelta
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
import plotly.graph_objects as go

def train():
    csv_url="https://api.covid19india.org/csv/latest/case_time_series.csv"

    df = pd. read_csv(csv_url)
    df = df[["Date_YMD", "Daily Confirmed"]]

    df['Dates']=pd.to_datetime(df["Date_YMD"])
    df=df[['Dates','Daily Confirmed']]
    #df=df.set_index(['Dates'])
    date_yerterday = datetime.today()-timedelta(days=1)

    train = df[(df['Dates']>=datetime(2020,3,15)) & (df['Dates']<=date_yerterday-timedelta(days = 5))]
    test = df[(df['Dates']>=date_yerterday-timedelta(days=4)) & (df['Dates']<=date_yerterday)]

    train=train.set_index('Dates')

    test=test.set_index('Dates')

    model = statsmodels.tsa.arima_model.ARIMA(train, order=(2,1,5))
    model_fitted = model.fit()
    print(model_fitted.summary2())

    forecast_days = 12
    fc, se, conf = model_fitted.forecast(forecast_days, alpha=0.05)
    first_train_date = train.reset_index().iloc[0]["Dates"]
    first_test_date = test.reset_index().iloc[1]['Dates']
    forc_first_date = train.reset_index().iloc[-1]["Dates"]+timedelta(days=1)
    forc_dates = pd.date_range(start=forc_first_date,end=forc_first_date+timedelta(days=forecast_days-1))
    fc_series = pd.Series(fc, index=forc_dates)

    last_pred_date = train.reset_index().iloc[-1]["Dates"]
    pred_date = last_pred_date-timedelta(days=15)
    predicted = model_fitted.predict(start=pred_date, end = last_pred_date,typ="levels")
    pred_dates = pd.date_range(start=pred_date, end = last_pred_date)
    predicted = pd.Series(predicted, index=pred_dates)

    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=train.reset_index()["Dates"][len(train.reset_index()["Dates"])-20:],
            y=train["Daily Confirmed"][len(train.reset_index()["Dates"])-20:],
            name="Actual Covid Cases Per Day", 
            marker=dict(color="#1C263C")
        ),
    )

    fig.add_trace(
        go.Scatter(
            x=pred_dates,
            y=predicted,
            name="Model Prediction On Present Data",
            marker=dict(color="#B6C0D2")
        ),
    )
    fig.add_trace(
        go.Scatter(
            x=test.reset_index()["Dates"],
            y=test["Daily Confirmed"],
            name="Actual Number Of Cases After Model Starts Forcasting",
            mode = "markers",
            marker=dict(color="#455268")
        )
    )
    fig.add_trace(
        go.Scatter(
            x=forc_dates,
            y=fc_series,
            name="Model Predicting On Untrained Data",
            mode = "lines",
            marker=dict(color="#9CFF00")
        )
    )
    fig.update_layout(
        xaxis_title="Date",
        yaxis_title="Daily COVID 19 Cases",
        margin=dict(t=20, l=20, r=0, b=10)
    )
    fig.add_trace(
        go.Scatter(
            x=[test.reset_index().iloc[-1]["Dates"]+timedelta(days=2)],
            y=[fc_series[len(test)+2]],
            name="Tomorrows Covid Cases",
            mode="markers",
            marker={'color':'#B6C0D2', 'size':15}
        ),
    )
    return fc_series[len(test)+2], fig

def get_results():
    value, figure=train()
    return value, figure