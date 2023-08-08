import json
import requests
from Configurations import curs


class ConvertionException(Exception):
    pass


class Convertor:
    @staticmethod
    def get_price(quote: str, base: str, amount: str):
        if quote == base:
            raise ConvertionException(f'Невозможно перевести одну и ту же валюту {base}')

        try:
            quote_ticker = curs[quote]
        except KeyError:
            raise ConvertionException('Не удалось обработать валюту {quote}')

        try:
            base_ticker = curs[base]
        except KeyError:
            raise ConvertionException('Не удалось обработать валюту {base}')

        try:
            amount = float(amount)
        except ValueError:
            raise ConvertionException('Не удалось обработать количество валюты {amount}')
        r = requests.get(f'https://min-api.crypto compare.com/data/price?fsym={quote_ticker}&tsyms={base_ticker}')
        total_base = json.loads(r.content)[curs[base]]
