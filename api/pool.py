import requests


class PoolApi:
    def __init__(self):
        self.URL = 'https://www.litecoinpool.org/api?api_key'

    def check_key(self, key):
        url = f'{self.URL}={key}'
        response = requests.get(url)
        if response.status_code != 200:
            return False
        return True

    def get_stats(self, key):
        url = f'{self.URL}={key}'
        response = requests.get(url)
        if response.status_code != 200:
            return False
        return response.json()
