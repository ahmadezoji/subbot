import hmac
import base64
import requests
import json
import urllib

APIURL = "https://api-swap-rest.bingbon.pro"
API_KEY = 'v29D1wyTsUbNLfinjqqgorjRV5nMyPJgrWye80AxnhiAQrP4wAo3RmU34otFehnHJcjOoZCLkJzLcNB5ZKyyQ'
SECRET_KEY = '96ou8MIZzN9mXgZVEjFxMLwWM4iDrivKJ4eDx3gYyZ4LR5F0yzrkvbUdgzpiX1p8EbVyC8qgHfC1Zyzqg'


def genSignature(path, method, paramsMap):
    sortedKeys = sorted(paramsMap)
    paramsStr = "&".join(["%s=%s" % (x, paramsMap[x]) for x in sortedKeys])
    paramsStr = method + path + paramsStr
    return hmac.new(SECRET_KEY.encode("utf-8"), paramsStr.encode("utf-8"), digestmod="sha256").digest()


def getLatestPrice(symbol):
    paramsMap = {
        "symbol": symbol,
    }
    paramsStr = "&sign=" + urllib.parse.quote(
        base64.b64encode(genSignature("/api/v1/market/getLatestPrice", "GET", paramsMap)))
    url = f'https://api-swap-rest.bingbon.pro/api/v1/market/getLatestPrice?&symbol={symbol}{paramsStr}'
    payload = {}
    headers = {
    }
    response = requests.request("GET", url, headers=headers, data=payload)
    last_price = (json.loads(response.text))['data']['tradePrice']
    last_price = float(last_price)
    return last_price
