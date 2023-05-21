import pickle
import requests
import pandas as pd
from config import API_KEY, API_SECRET


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

    def get_instrument_info(self, symbol, limit):
        endpoint = "/v5/market/instruments-info"
        params = {
            "category": 'spot',
            "symbol": symbol,
            "limit": limit
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
            if data['result']:
                return data['result']
            else:
                print("No items in kline data")
        except requests.exceptions.RequestException as e:
            print("An error occurred:", e)


# API KEY and API SECRET come from config file.
bybit_api = BybitAPI(API_KEY, API_SECRET)

instrument_info = bybit_api.get_instrument_info('', 100)
df_instruments_info = pd.DataFrame(instrument_info)

kline_data = bybit_api.get_kline_data("BTCUSDT", "60", 10)
df_kline_data = pd.DataFrame(kline_data)


# Store objects on a disk
def save_object_to_file(filename, obj):
    with open(filename, 'wb') as file:
        pickle.dump(obj, file)


# Read objects into memory
def load_object_from_file(filename):
    with open(filename, 'rb') as file:
        objects = pickle.load(file)
        return objects


# Save objects to pickle file
save_object_to_file('instruments_info.pkl', df_instruments_info)
save_object_to_file('kline_data.pkl', df_kline_data)

# Load from pickle file stored objects
# Assign loaded objects to variables -> and have them into memory
instruments_info_loaded = load_object_from_file('instruments_info.pkl')
kline_data_loaded = load_object_from_file('kline_data.pkl')

# print(instruments_info_loaded.to_string())
# print(kline_data_loaded.to_string())
