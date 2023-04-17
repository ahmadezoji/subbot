import hmac
import hashlib
import base64
APIURL = "https://api-swap-rest.bingbon.pro"
API_KEY = 'v29D1wyTsUbNLfinjqqgorjRV5nMyPJgrWye80AxnhiAQrP4wAo3RmU34otFehnHJcjOoZCLkJzLcNB5ZKyyQ'
SECRET_KEY = '96ou8MIZzN9mXgZVEjFxMLwWM4iDrivKJ4eDx3gYyZ4LR5F0yzrkvbUdgzpiX1p8EbVyC8qgHfC1Zyzqg'


def genSignature(path, method, paramsMap):
    sortedKeys = sorted(paramsMap)
    paramsStr = "&".join(["%s=%s" % (x, paramsMap[x]) for x in sortedKeys])
    paramsStr = method + path + paramsStr
    return hmac.new(SECRET_KEY.encode("utf-8"), paramsStr.encode("utf-8"), digestmod="sha256").digest()


