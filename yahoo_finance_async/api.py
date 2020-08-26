import asyncio
import json
import datetime
from enum import Enum

import aiohttp


class APIError(Exception):
    pass


class History(Enum):
    """Defines the possible historical time ranges to be fetched."""

    DAY = "1d"
    FIVE_DAYS = "5d"
    MONTH = "1mo"
    QUARTER = "3mo"
    HALF_YEAR = "6mo"
    YEAR = "1y"
    TWO_YEARS = "2y"
    FIVE_YEARS = "5y"
    TEN_YEARS = "10y"
    YTD = "ytd"
    MAX = "max"


class Interval(Enum):
    """Defines the possible lengths of each candle (OHLC) period."""

    MINUTE = "1m"
    TWO_MINUTE = "2m"
    FIVE_MINUTE = "5m"
    FIFTEEN_MINUTE = "15m"
    THIRTY_MINUTE = "30m"
    HOUR = "1h"
    DAY = "1d"
    FIVE_DAY = "5d"
    WEEK = "1wk"
    MONTH = "1mo"
    THREE_MONTH = "3mo"


class OHLC:
    """API call to fetch the OHLC candles."""

    base_url = "https://query1.finance.yahoo.com/v8/finance/chart/"
    base_params = {
        "events": "history",
    }

    @classmethod
    async def fetch(
        cls,
        symbol: str,
        interval: Interval = Interval.DAY,
        history: History = History.MONTH,
        **kwargs,
    ) -> dict:
        """An async method that fetches the OHLC data, parses it and returns as a list of candles.

        Parameters:
        - symbol - the name of the stock on Yahoo Finance e.g. AAPL, AV.L
        - interval - the length of the candles (an Interval Enum)
        - history - how far to go back to fetch candles (a History Enum)

        Return format:
        {
            "candles":
            [
                {datetime: candle_open_date, "open": 232, "high": 236.5, "low": 213.44, "close": 225.45, "volume": 34.2},
                {...}
            ],
            "meta" : the list of meta data returned by the API for checking purposes
        }
        """
        if not isinstance(interval, Interval):
            raise APIError(
                f"The 'interval' parameter must be an instance of the Interval Enum object."
            )
        if not isinstance(history, History):
            raise APIError(
                f"The 'history' parameter must be an instance of the History Enum object."
            )

        params = cls.base_params.copy()
        params.update({"interval": interval.value, "range": history.value})
        params.update(kwargs)

        url = cls.base_url + symbol

        response = await cls.raw_fetch(url, params)

        candles, meta = cls.parse_ohlc(response)

        return {"candles": candles, "meta": meta}

    @classmethod
    async def raw_fetch(cls, url, params) -> dict:
        """Fetches from the API and returns the response in the original format.
        Does basic error checking."""

        async with aiohttp.ClientSession() as session:

            async with session.get(url, params=params) as response:

                try:
                    response = await response.text()
                    return json.loads(response)

                except Exception as e:
                    raise APIError(f"Yahoo Finance API error - {e}")

    @classmethod
    def parse_ohlc(cls, response: dict) -> tuple:
        """Converts the response into a list of candle dictionaries.
        Returns the parsed candles and the meta data."""
        try:
            errors = response["chart"]["error"]
            if errors:
                raise APIError(
                    f"Yahoo Finance API responded with a specific error - {errors}"
                )
            result = response["chart"]["result"][0]

            meta = result["meta"]

            # Convert timestamps to datetimes
            timestamps = [
                datetime.datetime.utcfromtimestamp(x) for x in result["timestamp"]
            ]
            indicators = result["indicators"]["quote"][0]

            # Now turn into candle dictionaries
            candles = []
            for time, open, high, low, close, volume in zip(
                timestamps,
                indicators["open"],
                indicators["high"],
                indicators["low"],
                indicators["close"],
                indicators["volume"],
            ):
                candles.append(
                    {
                        "datetime": time,
                        "open": float(open),
                        "high": float(high),
                        "low": float(low),
                        "close": float(close),
                        "volume": float(volume),
                    }
                )

            return candles, meta

        except Exception as e:
            raise APIError(
                f"Unable to parse the OHLC candle data from the Yahoo Finance API response - {e}"
            )
