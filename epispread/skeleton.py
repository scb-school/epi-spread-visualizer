import pandas as pd
import numpy
import geopandas as gpd
import requests
import os

try:
    from graph_classes.heat_map import HeatMap
    from graph_classes.time_series import TimeSeries  # this should work when running table.py directly
except:
    # this should work when running main.py (it's a relative import)
    from .graph_classes.heat_map import HeatMap
    from .graph_classes.time_series import TimeSeries

# compatible with all data at https://covid19.who.int/data


class EpiSpread:
    urls = [
        'https://covid19.who.int/WHO-COVID-19-global-data.csv',
        'https://covid19.who.int/WHO-COVID-19-global-table-data.csv',
        'https://covid19.who.int/who-data/vaccination-data.csv',
        'https://covid19.who.int/who-data/vaccination-metadata.csv',
    ]

    @classmethod
    def _get_files(cls, urls, file_path=""):
        """This function grabs 4 specified URLs from https://covid19.who.int/data \
            and stores them as CSV files in data_files/[file_name]
        Returns 1 if failure, 0 if success

        Args:
            urls (list[str]): list of all website links to the files we want to download.

        Returns:
            list[str]: list of file names that get handed to the query. 
        """

        file_names = []

        for url in urls:
            r = requests.get(url, allow_redirects=True)
            if r.status_code == 200:
                if not file_path:
                    file_name = url.split('/')[-1].replace(".csv", "")
                    file_names.append(file_name)
                    if not os.path.exists("data_files"):
                        os.makedirs("data_files")
                    open('data_files/' + file_name + '.csv', 'wb').write(r.content)
                else:
                    open(file_path, 'wb').write(r.content)

        return file_names

    @classmethod
    def _read_data(cls, file_name):
        """read_data takes in a csv file name containing a dataset and reads it into a pandas DataFrame.
        Also reads the inbuilt "world" file in the gpd library into a GeoDataFrame.

        Args:
            file_name (str): name of file containing dataset

        Returns:
            (DataFrame, GeoDataFrame): Tuple of the pandas DataFrame of the data you entered, and the world GeoDataFrame
        """
        df = pd.read_csv(file_name, delimiter=",")
        world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))
        world = world[world.name != "Antarctica"]
        return df, world

    @classmethod
    def _find_time_series(cls, df, str_column, date_columns):
        """This function takes in a certain column of the dataframe and checks if it is eligible for a time series based on any of the date columns.
        If so, it returns the first valid data column. If not, returns None

        Args:
            df (DataFrame): pandas DataFrame we're parsing
            str_column (str): name of the qualitative column we're testing
            date_columns (list[str]): list of names of date columns within the dataframe.

        Returns:
            str: returns the name of the valid DataFrame column.
        """
        first_country = df[str_column].iloc[0]
        single_country = df.loc[df[str_column] == first_country]
        for date_column in date_columns:
            dates_of_country = list(single_country[date_column])
            if len(set(dates_of_country)) == len(dates_of_country) and len(dates_of_country) > 1:
                return date_column
        return None

    @classmethod
    def _parse_columns(cls, df):
        """This function parses the columns of a given DataFrame and seperates them into those with number values, those with dates, and those that are string entries

        Args:
            df (DataFrame): pandas DataFrame to be parsed

        Returns:
            list[str]: Names of columns with number values
            list[str]: Names of columns with date values
            list[str]: Names of columns with string values
        """
        time_series_columns = []
        number_columns = [
            df.columns[i]
            for i in range(0, len(df.columns))
            if isinstance(df.iloc[0, i], numpy.int64) or isinstance(df.iloc[0, i], numpy.float64)
        ]
        date_columns = [column for column in df.columns if "date" in column.lower()]
        iso_columns = [column for column in df.columns if "iso" in column.lower() or "code" in column.lower()]
        str_columns = list(set(df.columns).difference(number_columns + date_columns + iso_columns))
        for str_column in str_columns:
            time_series_column = cls._find_time_series(df, str_column, date_columns)
            if time_series_column:
                time_series_columns.append([str_column, time_series_column])

        return number_columns, date_columns, iso_columns, time_series_columns

    @classmethod
    def _find_available_graphs(cls, number_columns, iso_columns, time_series_columns):
        """find_available_graphs takes in the types of columns a dataset has and based on those,
        outputs a list of possible visualizations that can be graphed using the dataset's data.

        Args:
            number_columns (list[str]): list of column names within dataset that contain number values
            iso_columns (list[str]): list of column names within dataset that contain ISO values
            time_series_columns (list[str]): list of column names within dataset that contain date values

        Returns:
            list[str]: list of names of types of graphs that can be plotted with the
            available data types.
        """
        available_graphs = []
        if number_columns and iso_columns:
            available_graphs.append("heat map")
        if number_columns and iso_columns and time_series_columns:
            available_graphs.append("heat map w/ time slider")
        if time_series_columns:
            available_graphs.append("time series")
        return available_graphs

    @classmethod
    def run_query(cls):
        """This function is the only function that should be called by a user.
        run_query runs a user prompt in order to automate graph setup and creation.

        Returns:
            HeatMap: returns instance of HeatMap class if a HeatMap was plotted
            TimeSeries: returns instance of TimeSeries class if a TimeSeries was plotted.
        """
        file_names = cls._get_files(cls.urls)
        if not file_names:
            print("File retrieval failed.")
            return 1
        print("Available files:")
        print(file_names)
        file_name = "data_files/" + input("Which file do you want to analyze? ") + ".csv"
        df, world = cls._read_data(file_name)

        number_columns, date_columns, iso_columns, time_series_columns = cls._parse_columns(df)

        print(cls._find_available_graphs(number_columns, iso_columns, time_series_columns))
        graph_type = input("What type of data visualization do you want to create?")
        print(number_columns)
        indep_var = input("Which variable do you want to plot in your " + graph_type + "?")
        if graph_type == "heat map w/ time slider" or graph_type == "heat map":
            if graph_type == "heat map w/ time slider":
                print([time_series_column[1] for time_series_column in time_series_columns])
                time_series_column = input("Which time series would you like to plot?")
                start_date = input(
                    "Which date would you like to start plotting from?\nPlease format it YYYY-MM-DD, and it cannot be earlier than "
                    + df[time_series_column].iloc[0]
                    + "."
                )
                graph_inst = HeatMap(df, world, indep_var, start_date, iso_columns[0], time_series_column, ts_flag=1)
            else:
                graph_inst = HeatMap(df, world, indep_var, df[date_columns[0]].iloc[0], iso_columns[0], date_columns[0])
        elif graph_type == "time series":
            print(time_series_columns)
            my_time_series = input("Which time series would you like to plot?")
            time_series_list = my_time_series.strip("]").strip("[").replace("'", "").replace(",", "").split(" ")
            graph_inst = TimeSeries(df, time_series_list[1], time_series_list[0], indep_var)

        graph_inst.plot()
        return graph_inst


def main():
    EpiSpread.run_query()
    # df = pd.read_csv("data_files/WHO-COVID-19-global-data.csv", delimiter=",")
    # test = TimeSeries(df, "Date_reported", "Country", "Cumulative_cases")
    # test.arrange_data()


if __name__ == "__main__":
    main()
