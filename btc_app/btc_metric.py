import logging
from prometheus_client import start_http_server, Gauge
import time
import requests as r


def create_logger():
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - [%(levelname)s]: %(message)s',
        handlers=[
            logging.FileHandler('btc_val.log'),
            logging.StreamHandler()
        ]
    )

    log = logging.getLogger('BTC_APP')
    return log


def update_metric():
    btc = get_btc_val()
    btc_val_gauge.set(btc)
    log.info('Updated BTC value gauge to %s', btc)

def get_btc_val():
    try:
        res = r.get('https://blockchain.info/ticker')
        res.raise_for_status()
        currencyDict = res.json()

        btc_val = currencyDict['USD']['last']
        log.info('The current BTC value is %s', btc_val)
        return btc_val
    except r.exceptions.RequestException as e:
        log.error('Error fetching BTC value: %s', e)
        return None

if __name__ == '__main__':
    log = create_logger()

    start_http_server(8000)

    btc_val_gauge = Gauge('btc_val', 'Bitcoin value in USD')
    log.info('HTTP server started on port 8000')

    while True:
        update_metric()
        time.sleep(60)
