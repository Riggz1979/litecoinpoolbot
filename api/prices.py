import requests


class Prices:
    def __init__(self):
        self.URL = 'https://api.coingecko.com/api/v3/simple/price?ids='

    def get_price(self, currency, fiat):
        url = f'{self.URL}{currency}&vs_currencies={fiat}'
        response = requests.get(url)
        if response.status_code == 200:
            if response.json() and response.json()[currency]:
                return response.json()[currency][fiat]
            return 0
        return f'Overload {response.status_code}'

    def get_most_popular(self):
        url = f'{self.URL}bitcoin,litecoin,dogecoin,ethereum&vs_currencies=usd'
        print(url)
        response = requests.get(url)
        if response.status_code == 200:
            prices = {}
            for resp in response.json():
                prices[resp] = response.json()[resp]['usd']
            return prices
        else:
            print(f'Error: {response.status_code}')


if __name__ == '__main__':
    price = Prices()
    print(price.get_most_popular())

