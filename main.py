import time
import requests


def getBTC():
    import requests

    url = "https://quotient.p.rapidapi.com/equity/live"

    querystring = {"symbol": "BTC", "timezone": "UTC"}

    headers = {
        "X-RapidAPI-Key": "1fef60786cmshd959f31807f69dbp1f6649jsnb1ea086a8e4a",
        "X-RapidAPI-Host": "quotient.p.rapidapi.com"
    }

    response = requests.request("GET", url, headers=headers, params=querystring)

    print(response.text)
    return response.text

if __name__ == '__main__':
    getBTC()


