from unittest.mock import MagicMock, Mock, patch
from epispread import EpiSpread
from matplotlib.widgets import Slider
import pandas as pd
import geopandas as gpd

mock_df = MagicMock(spec=pd.DataFrame)
mock_df_index = MagicMock(spec=list)

thing = EpiSpread()


def test_read_data():
    mock_world = Mock(spec=gpd.GeoDataFrame)
    assert type(thing.read_data()[0]) is mock_df.__class__
    assert type(thing.read_data()[1]) is mock_world.__class__


def test_slider_setup():
    mock = Mock(spec=Slider)
    assert type(thing.slider_setup()) is mock.__class__


@patch('country_converter.convert')
def test_iso2_to_iso3(mock_convert):
    mock_convert.return_value = "test"
    with patch.object(pd, 'DataFrame', {"Country_code": ['AF', 'AL', 'DZ']}):
        thing.iso2_to_iso3(pd.DataFrame["Country_code"])
    mock_convert.assert_called_once()


def test_add_iso3():
    thing.iso2_to_iso3 = MagicMock(return_value=['AFG', 'ALB', 'DZA'])
    with patch.object(thing, 'df', pd.DataFrame(['AF', 'AL', 'DZ'], columns=['Country_code']), spec=True):
        thing.add_iso3(thing.df)
    thing.iso2_to_iso3.assert_called_once()


@patch('pandas.DataFrame.copy')
def test_filter_single_date(mock_copy):
    with patch.object(thing, 'df', pd.DataFrame(['2020-01-21'], columns=['Date_reported'])):
        thing.filter_single_date('2020-01-21')
    mock_copy.assert_called_once()


@patch('pandas.merge')
def test_merge_manager(mock_merge):
    thing.filter_single_date = MagicMock(return_value=pd.DataFrame(['AF', 'AL', 'DZ'], columns=['Country_code']))
    thing.add_iso3 = MagicMock(return_value=pd.DataFrame(['2020-01-21'], columns=['Date_reported']), __spec__=True)
    thing.merge_manager('2020-01-21')
    thing.add_iso3.assert_called_once()
    thing.filter_single_date.assert_called_once()
    mock_merge.assert_called_once()
