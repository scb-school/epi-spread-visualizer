import pandas as pd
import geopandas as gpd
import country_converter as coco
import matplotlib.pyplot as plt
import datetime
from matplotlib.widgets import Slider

from mpl_toolkits.axes_grid1 import make_axes_locatable
 
FILE = "./WHO-COVID-19-global-data.csv"
START_DATE = '2020-01-21'
START_DATETIME = datetime.datetime.strptime(START_DATE, '%Y-%m-%d')

#matplotlib global vars
fig, ax = plt.subplots()
ax.set_aspect('equal')
divider = make_axes_locatable(ax)
cax = divider.append_axes("right", size="5%", pad=0.1)

def read_data():
    df = pd.read_csv(
        FILE, delimiter=",")
    world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))
    world = world[world.name != "Antarctica"]
    return df, world

def slider_setup():
    axcolor = 'lightgoldenrodyellow'
    axfreq = plt.axes([0.2, 0.1, 0.3, 0.03], facecolor=axcolor)
    return Slider(axfreq, START_DATE, 0.0, 300.0, valinit=0.0, valstep=20)

def iso2_to_iso3(iso2_codes):
    return coco.convert(names = iso2_codes, to='ISO3')

def add_iso3(df):
    iso3_codes = iso2_to_iso3(df['Country_code'])
    df.loc[:,'Country_code_iso3'] = iso3_codes
    return df
    
def filter_single_date(df, date):
    return df.loc[df['Date_reported'] == date].copy()

def merge_manager(df, date):
    mod_df = add_iso3(filter_single_date(df, date))
    merge = pd.merge(left=world, right=mod_df, left_on='iso_a3', right_on='Country_code_iso3', how='left')
    return merge.plot(ax = ax, column = 'Cumulative_cases', legend = True, cax = cax, missing_kwds={
            "color": "lightgrey",
            "edgecolor": "red",
            "hatch": "///",
            "label": "Missing values",
       },)
    
def update(time_offset):
    new_datetime = START_DATETIME + datetime.timedelta(days=time_offset)
    merge_graph = merge_manager(df, new_datetime.strftime('%Y-%m-%d'))
    fig.canvas.draw_idle()
    fig.canvas.flush_events()
    
df, world = read_data()
time_slider = slider_setup()

#callback
time_slider.on_changed(update)

#initial plot
merge_graph = merge_manager(df, START_DATE)
plt.show()
