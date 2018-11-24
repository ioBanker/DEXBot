from dexbot.strategies.external_feeds.process_pair import split_pair, debug
import requests
import asyncio

WAVES_URL = 'https://marketdata.wavesplatform.com/api/'
SYMBOLS_URL = "/symbols"
MARKET_URL = "/ticker/"


async def get_json(url):
    r = requests.get(url)
    json_obj = r.json()
    return json_obj


def get_last_price(base, quote):
    current_price = None
    try:                
        market_bq = MARKET_URL + quote  +'/'+ base # external exchange format
        ticker = asyncio.get_event_loop().run_until_complete(get_json(WAVES_URL + market_bq))
        current_price = ticker['24h_close']        
    except Exception as e:       
        pass  # No pair found on waves dex for external price. 
    return current_price


def get_waves_symbols():
    symbol_list = asyncio.get_event_loop().run_until_complete(get_json(WAVES_URL + SYMBOLS_URL))
    return symbol_list


def get_waves_by_pair(pair):
    current_price = get_last_price(pair[1], pair[0]) # base, quote
    if current_price is None: # try inversion
        price = get_last_price(pair[0], pair[1])
        if price is not None:
            current_price = 1/float(price)        
    return current_price


def get_waves_price(**kwargs):
    price = None
    for key, value in list(kwargs.items()):
        debug("The value of {} is {}".format(key, value))
        if key == "pair_":
            price = get_waves_by_pair(value)
            debug(value, price)
        elif key == "symbol_":
            pair = split_pair(value)
            price = get_waves_by_pair(pair)
            debug(pair, price)
    return price
    
