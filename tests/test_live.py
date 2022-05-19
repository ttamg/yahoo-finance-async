import datetime

import pytest
from yahoo_finance_async import OHLC, History, Interval


@pytest.mark.asyncio
async def test_raw_live():
    """A live call"""

    response = await OHLC.raw_fetch(
        url="https://query1.finance.yahoo.com/v8/finance/chart/AAPL", params={}
    )
    print(response)
    assert isinstance(response, dict)
    assert isinstance(response["chart"]["result"][0]["timestamp"], list)


@pytest.mark.asyncio
async def test_live():
    """A live call"""

    result = await OHLC.fetch(
        symbol="MSFT", interval=Interval.WEEK, history=History.QUARTER
    )
    print(result)
    assert isinstance(result, dict)
    meta = result["meta"]
    assert meta["symbol"] == "MSFT"
    assert isinstance(result["candles"], list)
    assert 10 < len(result["candles"]) < 20
    candle = result["candles"][5]
    assert isinstance(candle["datetime"], datetime.datetime)
    assert isinstance(candle["close"], float)


@pytest.mark.asyncio
async def test_live_with_none_values():
    """A live call - GTX stock has None values."""

    result = await OHLC.fetch(
        symbol="GTX", interval=Interval.FIFTEEN_MINUTE, history=History.MONTH
    )
    print(result)
    assert isinstance(result, dict)
    meta = result["meta"]
    assert meta["symbol"] == "GTX"
    # Confirm we get multiple of candles and it is not curtailed
    assert len(result["candles"]) > 4 * 7 * 10
