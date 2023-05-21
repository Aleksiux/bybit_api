import pickle
import requests
import pandas as pd
from config import API_SECRET, API_KEY


class InstrumentInfo:
    def __init__(self):
        self.symbol = []
        self.base_coin = []
        self.quote_coin = []
        self.innovation = []
        self.status = []
        self.lot_size_filter = []
        self.price_filter = []

    def add_items_in_instrument_info_class(self, instrument_info_data):
        """
        instrument_info_data: Comes from json request and adds to class hierarchy
        """
        for item in instrument_info_data:
            self.symbol.append(item['symbol'])
            self.base_coin.append(item['baseCoin'])
            self.quote_coin.append(item['quoteCoin'])
            self.innovation.append(item['innovation'])
            self.status.append(item['status'])
            self.lot_size_filter.append(item['lotSizeFilter'])
            self.price_filter.append(item['priceFilter'])

    def __str__(self):
        return f"Symbol: {self.symbol}\nBase Coin: {self.base_coin}\nQuote Coin: {self.quote_coin}\n" \
               f"Innovation: {self.innovation}\nStatus: {self.status}\nLot Size Filter: {self.lot_size_filter}\n" \
               f"Price Filter: {self.price_filter}"


class KlineData:
    def __init__(self, symbol):
        self.symbol = symbol
        self.data_list = []

    def add_items_in_kline_data_class(self, kline_data):
        """
        kline_data:  Comes from json request and adds to class hierarchy
        """
        for item in kline_data:
            self.data_list.append(item)

    def __str__(self):
        return f"Symbol: {self.symbol}\nData List: {self.data_list}"


class BybitAPI:
    def __init__(self, api_key, api_secret):
        self.base_url = "https://api-testnet.bybit.com"
        self.api_key = api_key
        self.api_secret = api_secret
        self.headers = {
            "Content-Type": "application/json",
            "api_key": self.api_key,
            "api_secret": self.api_secret
        }

    def get_instrument_info(self, symbol):
        endpoint = "/v5/market/instruments-info"
        params = {
            "category": 'spot',
            "symbol": symbol,
        }

        try:
            response = requests.get(self.base_url + endpoint, params=params, headers=self.headers)
            response.raise_for_status()
            data = response.json()
            if data['result']['list']:
                return data['result']['list']
            else:
                print("No items in instrument info")

        except requests.exceptions.RequestException as e:
            print("An error occurred:", e)

    def get_kline_data(self, symbol, interval, limit):
        endpoint = "/v5/market/kline"
        params = {
            "category": 'spot',
            "symbol": symbol,
            "interval": interval,
            "limit": limit
        }

        try:
            response = requests.get(self.base_url + endpoint, params=params, headers=self.headers)
            response.raise_for_status()
            data = response.json()
            if data['result']['list']:
                return data['result']['list']
            else:
                print("No items in kline data")
        except requests.exceptions.RequestException as e:
            print("An error occurred:", e)


# --------------------------------------------API_KEY / API_SECRET LOGIN -----------------------------------------------
"""
Login in with API_KEY and API_SECRET also extracting needed info (instrument_info and kline data) to json format
"""
bybit_api = BybitAPI(API_KEY, API_SECRET)


# -------------------------------------------Instrument data add--------------------------------------------------------

def instrument_data(instrument_data_symbol=''):
    """
    instrument_info_get: Getting data from json format and then adding instrument data to the class
    :param instrument_data_symbol: Symbol like BTCUSDT, ETHUSDT. By default, it's going to list everything.
    :return: returning to pandas dataframe
    """
    instrument_info_get = bybit_api.get_instrument_info(instrument_data_symbol)
    instrument_info = InstrumentInfo()
    instrument_info.add_items_in_instrument_info_class(instrument_info_get)
    data = {
        "symbol": instrument_info.symbol,
        "baseCoin": instrument_info.base_coin,
        "quoteCoin": instrument_info.quote_coin,
        "innovation": instrument_info.innovation,
        "status": instrument_info.status,
        "lotSizeFilter": instrument_info.lot_size_filter,
        "priceFilter": instrument_info.price_filter,
    }
    instrument_data_dataframe = pd.DataFrame(data)
    return instrument_data_dataframe


# ---------------------------------------------Kline add data-----------------------------------------------------------


def kline_data(kline_data_symbol, kline_data_interval, kline_data_limit=200):
    """
    kline_data_get: Getting data from json format and then adding kline data to the class
    :param kline_data_symbol: Only one symbol can be added like: BTCUSDT, ETHUSDT
    :param kline_data_interval: Kline interval. 1,3,5,15,30,60,120,240,360,720,D,M,W
    :param kline_data_limit: Limit for data size per page. [1, 200]. Default: 200
    :return:
    """
    kline_data_get = bybit_api.get_kline_data(kline_data_symbol, kline_data_interval, kline_data_limit)
    kline_data = KlineData(kline_data_symbol)
    kline_data.add_items_in_kline_data_class(kline_data_get)
    data = {
        "symbol": kline_data.symbol,
        "list": kline_data.data_list,
    }
    kline_data_dataframe = pd.DataFrame(data)
    return kline_data_dataframe


# Store objects on a disk
def save_object_to_file(filename, obj):
    with open(filename, 'wb') as file:
        pickle.dump(obj, file)


# Read objects into memory
def load_object_from_file(filename):
    with open(filename, 'rb') as file:
        objects = pickle.load(file)
        return objects


kline_data_symbol = "BTCUSDT"
kline_data_interval = 60
kline_data_limit = 10

# Save objects to pickle file
save_object_to_file('instruments_info.pkl', instrument_data())
save_object_to_file('kline_data.pkl', kline_data(kline_data_symbol, kline_data_interval, kline_data_limit))

# Load from pickle file stored objects
# Assign loaded objects to variables -> and have them into memory
instruments_info_loaded = load_object_from_file('instruments_info.pkl')
kline_data_loaded = load_object_from_file('kline_data.pkl')

# print(instruments_info_loaded.to_string())
# print(kline_data_loaded.to_string())