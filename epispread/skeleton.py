import pandas as pd
import geopandas as gpd
import country_converter as coco
import matplotlib.pyplot as plt
import datetime
from matplotlib.widgets import Slider
from mpl_toolkits.axes_grid1 import make_axes_locatable


class EpiSpread:
    FILE = "./WHO-COVID-19-global-data.csv"
    START_DATE = '2020-01-21'
    START_DATETIME = datetime.datetime.strptime(START_DATE, '%Y-%m-%d')

    def read_data(self, file, world_url=''):
        if not file:
            df = pd.read_csv(self.FILE, delimiter=",")
        else:
            self.FILE = file
            df = pd.read_csv(file, delimiter=",")
        if not world_url:
            world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))
        else:
            world = pd.read_csv(world_url, delimiter=",")
        world = world[world.name != "Antarctica"]
        return df, world

    def __init__(self, file, world_url=''):
        # matplotlib global vars
        self.fig, self.ax = plt.subplots()
        self.ax.set_aspect('equal')
        self.divider = make_axes_locatable(self.ax)
        self.cax = self.divider.append_axes("right", size="5%", pad=0.1)
        self.df, self.world = self.read_data(file, world_url)

    def slider_setup(self):
        axcolor = 'lightgoldenrodyellow'
        axfreq = plt.axes([0.2, 0.1, 0.3, 0.03], facecolor=axcolor)
        return Slider(axfreq, self.START_DATE, 0.0, 300.0, valinit=0.0, valstep=20)

    def iso2_to_iso3(self, iso2_codes):
        return coco.convert(names=iso2_codes, to='ISO3')

    def add_iso3(self, df):
        iso3_codes = self.iso2_to_iso3(df['Country_code'])
        df.loc[:, 'Country_code_iso3'] = iso3_codes
        return df

    def filter_single_date(self, date):
        return self.df.loc[self.df['Date_reported'] == date].copy()

    def merge_manager(self, date):
        mod_df = self.add_iso3(self.filter_single_date(date))
        merge = pd.merge(left=self.world, right=mod_df, left_on='iso_a3', right_on='Country_code_iso3', how='left')
        return merge.plot(
            ax=self.ax,
            column='Cumulative_cases',
            legend=True,
            cax=self.cax,
            missing_kwds={
                "color": "lightgrey",
                "edgecolor": "red",
                "hatch": "///",
                "label": "Missing values",
            },
        )

    def update(self, time_offset):
        new_datetime = self.START_DATETIME + datetime.timedelta(days=time_offset)
        self.merge_manager(new_datetime.strftime('%Y-%m-%d'))
        self.fig.canvas.draw_idle()
        self.fig.canvas.flush_events()

    def plot_all(self):
        time_slider = self.slider_setup()

        # callback
        time_slider.on_changed(self.update)

        # initial plot
        self.merge_manager(self.START_DATE)
        plt.show()


def main():
    epi_instance = EpiSpread(EpiSpread.FILE)
    epi_instance.world.to_csv('world.csv', index=False)
    epi_instance.plot_all()


if __name__ == "__main__":
    main()
