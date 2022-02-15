import logging
import datetime
import pandas as pd
from bokeh.plotting import figure, output_file, show
from bokeh.models import LinearAxis, Range1d
from bnine.bnine import Fixerio


# Enter API key for fixer.io
API_KEY = None
# Change list of currencies
currency_str = 'USD,MXN'
# Historical rates (available from 1999)
start_date = datetime.datetime(2021, 7, 25) 
start_date = datetime.datetime(2022, 2, 10)
end_date = datetime.datetime.now() - datetime.timedelta(days=1)
FORMAT = "%Y-%m-%d"

def convert_dict_to_df(dict_cur):
    df_cur = pd.DataFrame(dict_cur, index=[0])
    return df_cur

fixer = Fixerio(API_KEY)
dfs = []

while start_date < end_date:
	response_cur = fixer.historical(start_date.strftime(FORMAT),currency_str)
	if response_cur['success']:
		response_cur['rates']['date'] = response_cur['date']
		dfs.append(convert_dict_to_df(response_cur['rates']))
	else:
		print(response_cur)
	start_date += datetime.timedelta(days=1)

if not dfs:
    raise SystemExit(1)

dfi = pd.concat(dfs)
dfi['date'] = pd.to_datetime(dfi['date'])

# Draw graph for EUR/USD, EUR/MXN
x_column = "date"
y_column1 = "EUR/USD"
y_column2 = "EUR/MXN"

df = pd.DataFrame()
df[x_column] = dfi['date']
df[y_column1] = dfi['USD']
df[y_column2] = dfi['MXN']

output_file("cur_USD-MXN.html")

y_overlimit = 0.05 # show y axis below and above y min and max value
p = figure(x_axis_type="datetime", plot_width=1000, plot_height=600)

p.line(df[x_column], df[y_column1], legend_label=y_column1, line_width=1, color="blue")
p.yaxis.axis_label = y_column1
p.y_range = Range1d(
    start=df[y_column1].min() * (1 - y_overlimit), 
    end=df[y_column1].max() * (1 + y_overlimit)
)

y_column2_range = y_column2 + "_range"
p.extra_y_ranges = {
    y_column2_range: Range1d(
        start=df[y_column2].min() * (1 - y_overlimit),
        end=df[y_column2].max() * (1 + y_overlimit),
    )
}
p.add_layout(LinearAxis(y_range_name=y_column2_range,axis_label=y_column2), "right")

p.line(
    df[x_column],
    df[y_column2],
    legend_label=y_column2,
    line_width=1,
    y_range_name=y_column2_range,
    color="green",
)

show(p)