import pandas as pd
import geopandas as gpd
import country_converter as coco
import matplotlib.pyplot as plt
import datetime
from matplotlib.widgets import Slider

from mpl_toolkits.axes_grid1 import make_axes_locatable
 
FILE_1 = "./time_series_covid19_confirmed_global.csv"
FILE_2 = "./WHO-COVID-19-global-data.csv"
START_DATE = '2020-01-21'
START_DATETIME = datetime.datetime.strptime(START_DATE, '%Y-%m-%d')
fig, ax = plt.subplots()
ax.set_aspect('equal')
divider = make_axes_locatable(ax)
cax = divider.append_axes("right", size="5%", pad=0.1)

def setup_manager():
    df = pd.read_csv(
        FILE_2, delimiter=",")
    world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))
    world = world[world.name != "Antarctica"]
    return df, world

df, world = setup_manager()

#matches names of column 2 to be those of column 1
def iso2_to_iso3(iso2_codes):
    return coco.convert(names = iso2_codes, to='ISO3')

def merge_manager(date):
    single_date_df = df.loc[df['Date_reported'] == date].copy()
    iso3_codes = iso2_to_iso3(single_date_df['Country_code'])
    single_date_df.loc[:,'Country_code_iso3'] = iso3_codes
    merge = pd.merge(left=world, right=single_date_df, left_on='iso_a3', right_on='Country_code_iso3', how='left')
    
    return merge.plot(ax = ax, column = 'Cumulative_cases', legend = True, cax = cax, missing_kwds={
            "color": "lightgrey",
            "edgecolor": "red",
            "hatch": "///",
            "label": "Missing values",
       },)
    
merge_graph = merge_manager(START_DATE)
axcolor = 'lightgoldenrodyellow'
axfreq = plt.axes([0.2, 0.1, 0.3, 0.03], facecolor=axcolor)
stime = Slider(axfreq, START_DATE, 0.0, 300.0, valinit=0.0, valstep=20)
    
    #print(merge.loc[merge["Date_reported"] == date]['Cumulative_cases'])
    #print(merge.is_empty)
    
    #print("af is " + merge.at[merge.loc[(merge["Country_code"] == "AF") & merge["Date_reported"] == date],'Cumulative_cases'])

def update(time_offset):
    new_datetime = START_DATETIME + datetime.timedelta(days=time_offset)
    merge_graph = merge_manager(new_datetime.strftime('%Y-%m-%d'))
    fig.canvas.draw_idle()
    fig.canvas.flush_events()
    
stime.on_changed(update)

plt.show()
