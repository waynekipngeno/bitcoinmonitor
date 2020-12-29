import requests
import time
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects 

from datetime import datetime

IFTTT_WEBHOOKS_URL = 'https://maker.ifttt.com/trigger/{}/with/key/pXHMMbIknso9fsULRdFcIWrLBEQZinEwe6xd4x4BEZM'

def get_latest_bitcoin_price():
    from coinmarketcapapi import CoinMarketCapAPI, CoinMarketCapAPIError
    cmc = CoinMarketCapAPI('12c31d0e-b406-4691-bace-51c4691d4477')
    r = cmc.cryptocurrency_listings_latest()
    return float(r.data[0]['quote']['USD']['price'])
def post_ifttt_webhook(event, value):
    # the payload will be sent to IFTTT service
    data = {'value1': value}
    # inserts our desired event
    ifttt_event_url = IFTTT_WEBHOOKS_URL.format(event)
    # sends a http POST request to the webhook url
    requests.post(ifttt_event_url, json=data)

def format_bitcoin_history(bitcoin_history):
    rows = []
    for bitcoin_price in bitcoin_history:
        # formats the date into a string 
        date = bitcoin_price['date'].strftime('%d.%m.%Y %H:%M')
        price = bitcoin_price['price']
        row  = '{}: $<b>{}</b>'.format(date, price)
        rows.append(row)
    # Use a <br> (break) tag to create a new line
    # Join the rows delimited by <br> tag: row1<br>row2<br>row3
    return '<br>'.join(rows)

BITCOIN_PRICE_THRESHOLD = 10000 

def main():
    bitcoin_history = []
    while True:
        price = get_latest_bitcoin_price()
        date = datetime.now()
        bitcoin_history.append({'date':date, 'price':price})

        # send emergency notifications
        if price < BITCOIN_PRICE_THRESHOLD:
            post_ifttt_webhook('bitcoin_price_emergency', price)

        # send a Telegram notifications
        # Once we have 5 items in our bitcoin_history send an update
        if len(bitcoin_history) == 5:
            post_ifttt_webhook('bitcoin_price_update', format_bitcoin_history(bitcoin_history))

            # reset the history
            bitcoin_history = []
        # sleep for 5 minutes
        time.sleep(2*60)
    
if __name__ == "__main__":
    main()