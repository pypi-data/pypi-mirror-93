"""
utils_coinbase.py
"""
import sys
from typing import List
import time
import asyncio
from datetime import datetime, timedelta

import pandas as pd
from aiohttp import ClientSession
import requests


async def _get_current_price(type='buy', currency_pair='BTC-USD', date=None, session=None):
    if date is None:
        date = datetime.now().strftime('%Y-%m-%d')
    available_type = ['buy', 'sell', 'spot']
    BASE_URL = 'https://api.coinbase.com/v2/prices/'
    if currency_pair is not None:
        url = '{}{}/'.format(BASE_URL, currency_pair)
    else:
        print('Error: currency_pair is None')
        sys.exit(1)
    if type in available_type:
        url = '{}{}'.format(url, type)
    else:
        print('Error: type not available, try {}'.format(available_type))
        sys.exit(1)
    if date is not None:
        url = '{}?date={}'.format(url, date)
    try:
        async with session.get(url) as response:
            if response.status != 200:
                print('status_code {} for url {}'.format(response.status, url))
            else:
                json = response.json()
                return await json
    except Exception as e:
        print('Not able to get {}, {}'.format(url, e))
        return {}


def _get_current_price_loop(type='buy', currency_pair='BTC-USD', date=None, session=None):
    if date is None:
        date = datetime.now().strftime('%Y-%m-%d')
    available_type = ['buy', 'sell', 'spot']
    BASE_URL = 'https://api.coinbase.com/v2/prices/'
    if currency_pair is not None:
        url = '{}{}/'.format(BASE_URL, currency_pair)
    else:
        print('Error: currency_pair is None')
        sys.exit(1)
    if type in available_type:
        url = '{}{}'.format(url, type)
    else:
        print('Error: type not available, try {}'.format(available_type))
        sys.exit(1)
    if date is not None:
        url = '{}?date={}'.format(url, date)
    try:
        response = requests.get(url)
        if response.status_code != 200:
            print('status_code {} for url {}'.format(response.status_code, url))
        else:
            json = response.json()
            return json
    except Exception as e:
        print('Not able to get {}, {}'.format(url, e))
        return {}


async def future_price(dates: List[str], type, currency_pair) -> object:
    """
    Async function to do API call faster.
    input:
            :mdls: list, models we want ratings
            :token: str, openvoice token to query the API
            :endpoint: str, endpoint from OPV API
    output:
            asyncio object
    """
    tasks = []
    async with ClientSession() as session:
        for date in dates:
            task = asyncio.ensure_future(_get_current_price(type=type,
                                                            currency_pair=currency_pair,
                                                            date=date,
                                                            session=session))
            tasks.append(task)

        return await asyncio.gather(*tasks)


def get_price_for_last_n_days(n=1, type='spot', currency_pair='BTC-USD'):
    print('Fetching {} ({}) data for the last {} days...'.format(type,
                                                                 currency_pair,
                                                                 n))
    start = time.time()
    dates = []
    prices = []
    jsons = []
    #loop = asyncio.get_event_loop()
    for i in range(n, -1, -1):
        date = (datetime.now() - timedelta(days=i)).strftime('%Y-%m-%d')
        dates.append(date)
        jsons.append(_get_current_price_loop(type=type,
                                             currency_pair=currency_pair,
                                             date=date))
    """
    future = asyncio.ensure_future(future_price(dates=dates,
                                                type=type,
                                                currency_pair=currency_pair))
    jsons = loop.run_until_complete(future)
    loop.close()
    """
    prices = [float(json.get('data', {'amount': 0})['amount'])
              if json else 0
              for json in jsons]

    data = pd.DataFrame({'date': dates,
                         'price': prices,
                         'timestamp': [i+1 for i in range(len(dates))]})
    print('Data fetched in {:.2f} s'.format(time.time() - start))
    return data