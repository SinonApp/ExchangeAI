import json
import requests
import time

class UnifyParser:

    def __init__(self, url, exchange, params={}, headers={}):
        # params example: {'json_head_param': 'items', 'items_params': ['symbol', 'last_price']}
        self.url = url
        self.exchange = exchange
        self.params = params
        self.headers = headers
        self.ts = int(time.time())

    def save_to_redis(self, redis, output):
        for item in output:
            last = 0
            if item['last_price'] != None:
                last = item['last_price']
            redis.set(f"prices:{self.ts}:{item['symbol']}:{self.exchange}", float(last))

    def parse_upbit(self, count_try=0):
        count_try = count_try + 1
        if count_try > 3:
            self.data = None
            return None
        markets = requests.get(url="https://api.upbit.com/v1/market/all", headers=self.headers)
        if markets.status_code == 200:
            markets = json.loads(markets.text)
            markets = [item['market'] for item in markets]
            self.params['markets'] = ','.join(markets)
            req = requests.get(url=self.url, params=self.params, headers=self.headers)
            if req.status_code == 200:
                self.data = json.loads(req.text)
                return self.data
            else:
                return self.parse_upbit(count_try=count_try)
        else:
            return self.parse_upbit(count_try=count_try)

    def parse(self, count_try=0):
        match self.exchange:
            case 'upbit':
                return self.parse_upbit(count_try=count_try)
            case _:
                count_try = count_try + 1
                if count_try > 3:
                    self.data = None
                    return None
                req = requests.get(url=self.url, params=self.params, headers=self.headers)
                if req.status_code == 200:
                    self.data = json.loads(req.text)
                    return self.data
                else:
                    return self.parse(count_try=count_try)
    
    def clear_symbols(self, symbol):
        return symbol.replace('/', '').replace('-', '').replace('_', '').replace(' ', '').upper()

    def format(self):
        output = []
        if self.data is None:
            return output
        match self.exchange:
            case 'binance':
                for item in self.data:
                    data = {}
                    data['symbol'] = self.clear_symbols(item['symbol'])
                    data['last_price'] = item['price']
                    output.append(data)
            case 'bybit':
                for item in self.data['result']:
                    data = {}
                    data['symbol'] = self.clear_symbols(item['symbol'])
                    data['last_price'] = item['last_price']
                    output.append(data)
            case 'coinsbit':
                for item in self.data['result']:
                    data = {}
                    data['symbol'] = self.clear_symbols(item)
                    data['last_price'] = self.data['result'][item]['ticker']['last']
                    output.append(data)
            case 'bitfinex':
                for item in self.data:
                    data = {}
                    data['symbol'] = self.clear_symbols(item[0])
                    data['last_price'] = item[7]
                    output.append(data)
            case 'mexc':
                for item in self.data:
                    data = {}
                    data['symbol'] = self.clear_symbols(item['symbol'])
                    data['last_price'] = item['price']
                    output.append(data)
            case 'kucoin':
                for item in self.data['data']['ticker']:
                    data = {}
                    data['symbol'] = self.clear_symbols(item['symbol'])
                    data['last_price'] = item['last']
                    output.append(data)
            case 'bitget':
                for item in self.data['data']:
                    data = {}
                    data['symbol'] = self.clear_symbols(item['symbol'])
                    data['last_price'] = item['close']
                    output.append(data)
            case 'lbank':
                for item in self.data['data']:
                    data = {}
                    data['symbol'] = item['symbol']
                    data['last_price'] = item['ticker']['latest']
                    output.append(data)
            case 'crypto':
                for item in self.data['ticker']:
                    data = {}
                    data['symbol'] = self.clear_symbols(item['symbol'])
                    data['last_price'] = item['last']
                    output.append(data)
            case 'bkex':
                for item in self.data['data']:
                    data = {}
                    data['symbol'] = self.clear_symbols(item['symbol'])
                    data['last_price'] = item['price']
                    output.append(data)
            case 'bitmart':
                for item in self.data['data']['tickers']:
                    data = {}
                    data['symbol'] = self.clear_symbols(item['symbol'])
                    data['last_price'] = item['last_price']
                    output.append(data)
            case 'upbit':
                for item in self.data:
                    data = {}
                    data['symbol'] = self.clear_symbols(item['market'])
                    data['last_price'] = item['trade_price']
                    output.append(data)
            case 'probit':
                for item in self.data['data']:
                    data = {}
                    data['symbol'] = self.clear_symbols(item['market_id'])
                    data['last_price'] = item['last']
                    output.append(data)
            case 'bittrex':
                for item in self.data:
                    data = {}
                    data['symbol'] = self.clear_symbols(item['symbol'])
                    data['last_price'] = item['lastTradeRate']
                    output.append(data)
            case 'okcoin':
                for item in self.data['data']:
                    data = {}
                    data['symbol'] = self.clear_symbols(item['instId'])
                    data['last_price'] = item['last']
                    output.append(data)
            case 'okx':
                for item in self.data['data']:
                    data = {}
                    data['symbol'] = self.clear_symbols(item['instId'])
                    data['last_price'] = item['last']
                    output.append(data)
            case 'poloniex':
                for item in self.data:
                    data = {}
                    data['symbol'] = self.clear_symbols(item['symbol'])
                    data['last_price'] = item['close']
                    output.append(data)
#            case 'exmo':
#                for item in self.data:
#                    if self.data != False or item != False:
#                        data = {}
#                        data['symbol'] = item
#                        data['last_price'] = self.data[item]['last_trade']
#                        output.append(data)

        return output