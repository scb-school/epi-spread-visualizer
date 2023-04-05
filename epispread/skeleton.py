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
        """This function will take in two distinct files in csv format and return both into pandas DataFrames using the pd.read_csv function.

        Args:
            file (str): Relative path to a csv with disease spread statistics across countries, delimited by either ISO2 or ISO3.
            world_url (str, optional): Relative path to a csv of world geography. Defaults to using the inbuilt geopandas version (this way is ideal).

        Returns:
            (DataFrame, DataFrame): Tuple of pandas DataFrames containing appropriate data.
        """
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
        """Sets up the slider on the graph.

        Returns:
            matplotlib.widgets.Slider: A slider representing a floating point range.
        """
        axcolor = 'lightgoldenrodyellow'
        axfreq = plt.axes([0.2, 0.1, 0.3, 0.03], facecolor=axcolor)
        return Slider(axfreq, self.START_DATE, 0.0, 300.0, valinit=0.0, valstep=20)

    def iso2_to_iso3(self, iso2_codes):
        """Takes a list of iso2 codes and outputs a list of iso3 codes using coco package.

        Args:
            iso2_codes (list): list of iso2 codes

        Returns:
            list: list of iso3 codes
        """
        return coco.convert(names=iso2_codes, to='ISO3')

    def add_iso3(self, df):
        """Takes in the given dataframe and adds a column of ISO3 codes based on the existing column of ISO2.

        Args:
            df (DataFrame): The DataFrame to add to.

        Returns:
            DataFrame: The inputted DataFrame with the added column.
        """
        iso3_codes = self.iso2_to_iso3(df['Country_code'])
        df.loc[:, 'Country_code_iso3'] = iso3_codes
        return df

    def filter_single_date(self, date):
        """Filters the DataFrame associated with the class instance by the specified date.

        Args:
            date (str): The date to filter on

        Returns:
            DataFrame: The appropriately filtered DataFrame.
        """
        return self.df.loc[self.df['Date_reported'] == date].copy()

    def merge_manager(self, date):
        """If necessary, converts the iso2 to iso3 in either DataFrame so they match. On the basis of the matching iso3 column, merges the two DataFrames and plots the resulting combination.

        Args:
            date (str): The required date, in format 'yy-mm-dd'

        Returns:
           (list of Line2D) : A list of lines representing the plotted data.
        """
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
        """"This is a callback function that replots the graph whenever time_offset is updated, a.k.a. whenever the slider on the map is moved. Takes in the time offset integer, converts to a real datetime, adds to the starting date and converts back to string to push to other methods.

        Args:
            time_offset (int): The associated number value of the slider, created in slider_setup.
        """
        new_datetime = self.START_DATETIME + datetime.timedelta(days=time_offset)
        self.merge_manager(new_datetime.strftime('%Y-%m-%d'))
        self.fig.canvas.draw_idle()
        self.fig.canvas.flush_events()

    def plot_all(self):
        """This function should be the only one getting called by the user. Will plot the merged DataFrame that results from the init method, along with a slider to show the progression of time.
        """
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
