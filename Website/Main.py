import dash_html_components as html
import dash
from covid import Covid
import pandas as pd
import statsmodels 
from datetime import datetime
from datetime import timedelta
import matplotlib.pyplot as plt
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
import plotly.graph_objects as go
import dash_core_components as dcc
import plotly.express as px



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

"""
residuals = pd.DataFrame(model_fitted.resid)
residuals.plot()
plt.show()
"""

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

stat = go.Figure()
stat.add_trace(
    go.Scatter(
        x=df["Dates"],
        y=df["Daily Confirmed"],
        marker=dict(color="#9CFF00")
        )
    )

stat.update_layout(
    xaxis_title="Date",
    yaxis_title="Daily COVID 19 Cases",
    margin=dict(t=0, l=0, r=0, b=0)
)

fig.update_layout(showlegend=False)

image = fig.write_image("assets/chart.png", width=1200, height=300, scale=2)
value = fc_series[len(test)+2:len(test)+7]

covid = Covid()
covid.get_data()
active = covid.get_total_active_cases()
confirmed = covid.get_total_confirmed_cases()
recovered = covid.get_total_recovered()
deaths = covid.get_total_deaths()

px.set_mapbox_access_token("pk.eyJ1IjoibmVldnRoZWdyZWF0ODc1IiwiYSI6ImNrc2lraW1jdjI0eTkydHFrbXltNWlmZXMifQ.Jp6wgaVqTc9UIucpIJ9gjg")
df=pd.read_csv("assets/dataset.csv")
fig2 = px.scatter_mapbox(df, lat="Latitude", lon="Longitude", color="State",hover_name="Name of the Vaccination Site*", hover_data=["State", "District", "Contact Person", "Mobile Number"]) 
app = dash.Dash(__name__)

app.layout =  html.Div([
    html.Div([html.H1("CoviBot", className="heading")], className="header"),
    html.Div([
        html.Div([html.H2("Vaccination Centers", className="mapTitle")], className="mapHeader"),
        html.Div([dcc.Graph(figure=fig2, style={'width': '100%', 'height': '100%'})], className="mapHolder")
        ], className="map"),
    html.Div([
        html.Div([html.H2("Covid Snapshots", className="generalTitle")], className="generalHeader"),
        html.Div([html.H2("Active:", className="generalHead"), html.H1(str(active), className="generalVal")], className="generalDivision"),
        html.Div([html.H2("Confirmed:", className="generalHead"), html.H1(str(confirmed), className="generalVal")], className="generalDivision"),
        html.Div([html.H2("Deaths:", className="generalHead"), html.H1(str(deaths), className="generalVal")], className="generalDivision"),
        html.Div([html.H2("Recovered:", className="generalHead"), html.H1(str(recovered), className="generalVal")], className="generalDivision"),
        html.Div([dcc.Graph(figure=stat, config={'displayModeBar': False}, style={'width': '100%', 'height': '100%'})], className="generalChartDiv")
        ], className="general"),
    html.Div([html.Div([html.H2("India Covid Forecast", className="forcastTitle")], className="forecastHeader"), html.Div([
        html.Div([html.H3(value.keys()[4].date()), html.H2(int(value[4]))], className="date"),
        html.Div([html.H3(value.keys()[3].date()), html.H2(int(value[3]))], className="date"),
        html.Div([html.H3(value.keys()[2].date()), html.H2(int(value[2]))], className="date"),
        html.Div([html.H3(value.keys()[1].date()), html.H2(int(value[1]))], className="date"),
        html.Div([html.H2(value.keys()[0].date(), className="tomText"), html.H1(int(value[0]), className="tomText")], className="tommDate")
        ], className="forcastInfoHead"), html.Div([dcc.Graph(id="graph", figure=fig, style={'width': '100%', 'height': '100%'})], className="forcastMapDiv")], className="forcast"),
    html.Div([html.Img(src=app.get_asset_url("discord-logo.png"), className="discordLogo"), html.A(href="https://discord.com/api/oauth2/authorize?client_id=859369537148813352&permissions=8&scope=bot", className="footerText", children="Get The Discord Bot")], className="footer")
])
app.title = 'CoviBot Website'

if __name__ == '__main__':
    app.run_server(debug=False)
