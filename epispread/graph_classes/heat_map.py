import pandas as pd
import country_converter as coco
import matplotlib.pyplot as plt
import datetime
from matplotlib.widgets import Slider
from mpl_toolkits.axes_grid1 import make_axes_locatable


class HeatMap:
    def __init__(self, df, world, plot_column, start_date, iso_column, date_column, ts_flag=0):
        self.df = df
        self.world = world
        self.plot_column = plot_column
        self.iso_column = iso_column
        self.date_column = date_column
        self.ts_flag = ts_flag

        self.start_date = start_date
        self.start_datetime = datetime.datetime.strptime(self.start_date, '%Y-%m-%d')

        self.fig, self.ax = plt.subplots()
        self.ax.set_aspect('equal')
        self.divider = make_axes_locatable(self.ax)
        self.cax = self.divider.append_axes("right", size="5%", pad=0.1)

    def _slider_setup(self):
        """Sets up the slider on the graph.

        Returns:
            matplotlib.widgets.Slider: A slider representing a floating point range.
        """
        axcolor = 'lightgoldenrodyellow'
        axfreq = plt.axes([0.2, 0.1, 0.3, 0.03], facecolor=axcolor)
        return Slider(axfreq, self.start_date, 0.0, 300.0, valinit=0.0, valstep=20)

    def _iso2_to_iso3(self, iso2_codes):
        """Takes a list of iso2 codes and outputs a list of iso3 codes using coco package.

        Args:
            iso2_codes (list): list of iso2 codes

        Returns:
            list: list of iso3 codes
        """
        return coco.convert(names=iso2_codes, to='ISO3')

    def _add_iso3(self, df):
        """Takes in the given dataframe and adds a column of ISO3 codes based on the existing column of ISO2.

        Args:
            df (DataFrame): The DataFrame to add to.

        Returns:
            DataFrame: The inputted DataFrame with the added column.
        """
        iso3_codes = self._iso2_to_iso3(df[self.iso_column])
        df.loc[:, 'Country_code_iso3'] = iso3_codes
        return df

    def _filter_single_date(self, date):
        """Filters the DataFrame associated with the class instance by the specified date.

        Args:
            date (str): The date to filter on

        Returns:
            DataFrame: The appropriately filtered DataFrame.
        """
        return self.df.loc[self.df[self.date_column] == date].copy()

    def _merge_manager(self, date):
        """If necessary, converts the iso2 to iso3 in either DataFrame so they match.
        On the basis of the matching iso3 column, merges the two DataFrames and plots the resulting combination.

        Args:
            date (str): The required date, in format 'yy-mm-dd'

        Returns:
           (list of Line2D) : A list of lines representing the plotted data.
        """
        if self.ts_flag:
            mod_df = self._filter_single_date(date)
        else:
            mod_df = self.df.copy()
        merge_iso_column = self.iso_column
        if len(self.df[self.iso_column].iloc[0]) == 2:
            mod_df = self._add_iso3(self._filter_single_date(date))
            merge_iso_column = 'Country_code_iso3'

        open('test.txt', 'w').write(str(mod_df))
        merge = pd.merge(left=self.world, right=mod_df, left_on='iso_a3', right_on=merge_iso_column, how='left')
        return merge.plot(
            ax=self.ax,
            column=self.plot_column,
            legend=True,
            cax=self.cax,
            missing_kwds={
                "color": "lightgrey",
                "edgecolor": "red",
                "hatch": "///",
                "label": "Missing values",
            },
        )

    def _update(self, time_offset):
        """ "This is a callback function that replots the graph whenever time_offset is updated,
        a.k.a. whenever the slider on the map is moved. Takes in the time offset integer, converts
        to a real datetime, adds to the starting date and converts back to string to push to other methods.

        Args:
            time_offset (int): The associated number value of the slider, created in slider_setup.
        """
        new_datetime = self.start_datetime + datetime.timedelta(days=time_offset)
        self._merge_manager(new_datetime.strftime('%Y-%m-%d'))
        self.fig.canvas.draw_idle()
        self.fig.canvas.flush_events()

    def plot(self):
        """This function should be the only one getting called by the user.
        Will plot the merged DataFrame that results from the init method, along with a slider to
        show the progression of time."""
        if self.ts_flag:
            time_slider = self._slider_setup()

            # callback
            time_slider.on_changed(self._update)

        # initial plot
        self._merge_manager(self.start_date)
        plt.show()
