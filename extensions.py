import json
import requests
from config import currencies


class ConvertionException(Exception):
    pass


class CurrencyConverter:
    @staticmethod
    def get_price(quote, base, amount):
        url = "https://currency-conversion-and-exchange-rates.p.rapidapi.com/convert"
        querystring = {}
        headers = {
            "X-RapidAPI-Key": "189297532emshe820e64aab4eeeep171e04jsn6069cb5a281c",
            "X-RapidAPI-Host": "currency-conversion-and-exchange-rates.p.rapidapi.com"
        }

        try:
            querystring["from"] = currencies[quote]
        except KeyError:
            raise ConvertionException('Неверное имя конвертируемой валюты. Введите доступную валюту')

        try:
            querystring["to"] = currencies[base]
        except KeyError:
            raise ConvertionException('Неверное имя итоговой валюты. Введите доступную валюту')

        if quote == base:
            raise ConvertionException('Указаны одинаковые валюты')

        try:
            type(float(amount))
        except ValueError:
            raise ConvertionException('Некорректно введена сумма конвертируемой валюты')

        querystring["amount"] = amount
        r = requests.get(url, headers=headers, params=querystring)
        api_res = json.loads(r.content)['result']
        return api_res
