#This example uses Python 2.7 and the python-request library.
import json
from coinmarketcapapi import CoinMarketCapAPI, CoinMarketCapAPIError

cmc = CoinMarketCapAPI('12c31d0e-b406-4691-bace-51c4691d4477')
r = cmc.cryptocurrency_listings_latest()

print(r.data[0]['quote']['USD']['price'])