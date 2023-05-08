import unittest
from matplotlib import pyplot as plt
import requests_mock
from unittest.mock import MagicMock, patch
from epispread import EpiSpread
from epispread.graph_classes.heat_map import HeatMap
from epispread.graph_classes.time_series import TimeSeries
from matplotlib.widgets import Slider
import pandas as pd
from pandas import DataFrame
from geopandas import GeoDataFrame
import os

mock_df_index = MagicMock(spec=list)

print(os.getcwd())


class EpiSpreadTests(unittest.TestCase):
    def test_get_files(self):
        mock_response = b'This is a mock file content'

        # Create a requests_mock instance
        with requests_mock.Mocker() as mocker:
            # Register the mock response for the requested URL
            mocker.get('https://example.com/file.csv', content=mock_response)

            # Call the function under test
            EpiSpread._get_files(['https://example.com/file.csv'], 'epispread/tests/data_files/file.csv')

            # Read the content of the downloaded file
            with open('epispread/tests/data_files/file.csv', 'rb') as f:
                downloaded_content = f.read()

            # Assert the content of the downloaded file
            self.assertEqual(downloaded_content, mock_response)

    def test_read_data(self):
        df, world = EpiSpread._read_data("epispread/tests/test-db.csv")
        self.assertIsInstance(df, DataFrame)
        self.assertIsInstance(world, GeoDataFrame)

    def test_find_time_series(self):
        test_df = pd.read_csv("epispread/tests/test-db.csv")
        result = EpiSpread._find_time_series(test_df, "Country", ["Date_reported"])
        self.assertEqual(result, "Date_reported")

    @patch('epispread.skeleton.EpiSpread._find_time_series')
    def test_parse_columns(self, mock_function):
        mock_function.return_value = "Time_series"

        test_df = pd.read_csv("epispread/tests/test-db.csv")
        number_columns, date_columns, iso_columns, time_series_columns = EpiSpread._parse_columns(test_df)
        self.assertEqual(number_columns[0], "New_cases")
        self.assertEqual(date_columns[0], "Date_reported")
        self.assertEqual(iso_columns[0], "Country_code")
        self.assertEqual(time_series_columns[0][1], "Time_series")

    def test_find_available_graphs(self):
        result = EpiSpread._find_available_graphs(1, 1, 1)
        self.assertIn("heat map", result)
        self.assertIn("heat map w/ time slider", result)
        self.assertIn("time series", result)

    # integration test
    def test_run_query(self):
        plt.switch_backend('Agg')
        with patch('builtins.input', side_effect=['WHO-COVID-19-global-data', 'heat map', 'New_cases']):
            plot = EpiSpread.run_query()
            self.assertIsInstance(plot, HeatMap)

        with patch(
            'builtins.input',
            side_effect=[
                'WHO-COVID-19-global-data',
                'heat map w/ time slider',
                'New_cases',
                'Date_reported',
                '2020-01-03',
            ],
        ):
            plot = EpiSpread.run_query()
            self.assertIsInstance(plot, HeatMap)

        with patch(
            'builtins.input',
            side_effect=['WHO-COVID-19-global-data', 'time series', 'New_cases', "['Country', 'Date_reported']"],
        ):
            plot = EpiSpread.run_query()
            self.assertIsInstance(plot, TimeSeries)


class HeatMapTests(unittest.TestCase):
    mock_df = MagicMock(spec=DataFrame)
    mock_world = MagicMock(spec=GeoDataFrame)
    plot_column = "New_cases"
    iso_column = "Country_code"
    date_column = "Date_reported"
    start_date = "2020-01-03"
    test_HeatMap = HeatMap(mock_df, mock_world, plot_column, start_date, iso_column, date_column)

    def test_slider_setup(self):
        result = self.test_HeatMap._slider_setup()
        self.assertIsInstance(result, Slider)

    @patch('epispread.graph_classes.heat_map.HeatMap._iso2_to_iso3')
    def test_add_iso3(self, mock_iso2_to_iso3):
        # self.test_HeatMap._iso2_to_iso3 = MagicMock(return_value=['AFG', 'ALB', 'DZA'])
        with patch.object(self.test_HeatMap, 'df', DataFrame(['AF', 'AL', 'DZ'], columns=['Country_code']), spec=True):
            self.test_HeatMap._add_iso3(self.test_HeatMap.df)
        mock_iso2_to_iso3.assert_called_once()

    @patch('country_converter.convert')
    def test_iso2_to_iso3(self, mock_convert):
        mock_convert.return_value = ['AFG', 'ALB', 'DZA']
        with patch.object(self.test_HeatMap, 'df', {"Country_code": ['AF', 'AL', 'DZ']}):
            iso3 = self.test_HeatMap._iso2_to_iso3(self.test_HeatMap.df["Country_code"])
        self.assertEqual(iso3, ['AFG', 'ALB', 'DZA'])
        mock_convert.assert_called_once()

    @patch('pandas.DataFrame.copy')
    def test_filter_single_date(self, mock_copy):
        with patch.object(self.test_HeatMap, 'df', DataFrame(['2020-01-21'], columns=['Date_reported'])):
            result = self.test_HeatMap._filter_single_date('2020-01-21')
        mock_copy.assert_called_once()

    @patch('pandas.merge')
    def test_merge_manager(self, mock_merge):
        self.test_HeatMap._filter_single_date = MagicMock(
            return_value=DataFrame(['AF', 'AL', 'DZ'], columns=['Country_code'])
        )
        self.test_HeatMap._add_iso3 = MagicMock(
            return_value=DataFrame(['2020-01-21'], columns=['Date_reported']), __spec__=True
        )
        self.test_HeatMap._merge_manager('2020-01-21')
        # self.test_HeatMap._add_iso3.assert_called_once()
        # self.test_HeatMap._filter_single_date.assert_called_once()
        mock_merge.assert_called_once()


class TimeSeriesTests(unittest.TestCase):
    @patch('pandas.to_datetime')
    @patch('pandas.pivot_table')
    def test_plot(self, mock_pivot, mock_datetime):
        test_df = pd.read_csv("epispread/tests/test-db.csv", delimiter=",")
        mock_pivot.return_value = test_df
        test_TimeSeries = TimeSeries(test_df, "Date_reported", "Country", "New_cases")
        self.assertFalse(test_TimeSeries.df.empty)
        self.assertGreater(len(test_TimeSeries.df), 0)
        self.assertIsInstance(test_TimeSeries, TimeSeries)


"""


class IntegrationTests(unittest.TestCase):
    integrate = ''

    @classmethod
    def setUpClass(cls) -> None:
        return super().setUpClass()

    def test_should_retrieve_dbs(self):
        self.integrate = EpiSpread(
            'epispread/tests/test-db.csv',
            'epispread/tests/test-world.csv',
        )
        self.assertIsNotNone(self.integrate.world)
        self.assertIsNotNone(self.integrate.df)
"""
