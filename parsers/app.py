from models import UnifyParser
from redis_om import get_redis_connection
import os

redis = get_redis_connection(
    host=os.getenv('REDIS_HOST'),
    port=os.getenv('REDIS_PORT'),
    decode_responses=True
)

dict_exchanges = {
    "binance": UnifyParser(url="https://api.binance.com/api/v3/ticker/price", exchange="binance"),
    "bybit": UnifyParser(url="https://api.bybit.com/v2/public/tickers", exchange="bybit"),
    'coinsbit': UnifyParser(url="https://api.coinsbit.io/api/v1/public/tickers", exchange="coinsbit"),
    'bitfinex': UnifyParser(url="https://api-pub.bitfinex.com/v2/tickers?symbols=ALL", exchange="bitfinex"),
    'okx': UnifyParser(url="https://www.okx.com/api/v5/market/tickers?instType=SPOT", exchange="okx"),
    'mexc': UnifyParser(url="https://api.mexc.com/api/v3/ticker/price?symbols=all", exchange="mexc"),
    'kucoin': UnifyParser(url="https://api.kucoin.com/api/v1/market/allTickers", exchange="kucoin"),
    'bitget': UnifyParser(url="https://api.bitget.com/api/spot/v1/market/tickers", exchange="bitget"),
    'lbank': UnifyParser(url="https://api.lbkex.com/v2/ticker/24hr.do?symbol=all", exchange="lbank"),
    'bkex': UnifyParser(url="https://api.bkex.com/v2/q/ticker/price", exchange="bkex"),
    'bitmart': UnifyParser(url="https://api-cloud.bitmart.com/spot/v2/ticker", exchange="bitmart"),
    'upbit': UnifyParser(url="https://api.upbit.com/v1/ticker", exchange="upbit", headers={'accept': 'application/json', 'content-type': 'application/json'}),
    'probit': UnifyParser(url="https://api.probit.com/api/exchange/v1/ticker", exchange="probit"),
    'bittrex': UnifyParser(url="https://api.bittrex.com/v3/markets/tickers", exchange="bittrex"),
    'okcoin': UnifyParser(url="https://www.okcoin.com/api/v5/market/tickers?instType=SPOT", exchange="okcoin"),
    'poloniex': UnifyParser(url="https://api.poloniex.com/markets/ticker24h", exchange="poloniex"),
    #'exmo': UnifyParser(url="https://api.exmo.com/v1.1/ticker", exchange="exmo"),
}

if __name__ == "__main__":
    for parser in dict_exchanges.values():
        parser.parse()
        output = parser.format()
        parser.save_to_redis(redis, output)
