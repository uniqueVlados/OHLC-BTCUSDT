from requests import get
from dataclasses import dataclass, asdict
from pydantic import validate_arguments
from datetime import datetime
import pandas
import plotly.graph_objects as pgo

BINANCE_API_HOST = "https://binance.com/"
API_PATH_BASE = "api/v1/"
KLINES_ENDPOINT = "klines"


@validate_arguments
@dataclass(frozen=True)
class Kline():
    open_time: datetime
    open: float
    high: float
    low: float
    close: float
    volume: float
    close_time: datetime
    quote_asset_volume: float
    number_of_trades: int
    taker_buy_base_asset_volume: float
    taker_buy_quote_asset_volume: float
    ignore: float


def get_klines(symbol: str, interval: str, limit: int):
    return get(
        url=BINANCE_API_HOST + API_PATH_BASE + KLINES_ENDPOINT,
        params={
            "symbol": symbol,
            "interval": interval,
            "limit": limit
        }
    ).json()


def build_plot(symbol: str, interval: str, limit: int) -> pgo.Figure:
    klines = pandas.DataFrame([asdict(Kline(*i))
                               for i in get_klines(symbol, interval, limit)])

    return pgo.Figure(
        data=[pgo.Candlestick(x=klines["open_time"],
                              open=klines['open'],
                              high=klines['high'],
                              low=klines['low'],
                              close=klines['close'])
              ]
    )

