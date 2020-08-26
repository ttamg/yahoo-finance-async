# yahoo-finance-async

A simple Python async API wrapper for the deprecated (but currently still working) Yahoo Finance API.

Although the Yahoo Finance API has officially been closed down, it does still work and it provides a free access to a vast number of stocks. 

> **Warning** - The Yahoo Finance API could be removed or shut down at any point.  You use this package at your own risk.


## Why async?

There are many Yahoo Finance API libraries available on PyPi which use synchronous functions.  There do not seem to be async functions available yet (as far as I could find).  I needed an async version for a simple project to collect candle data (OHLC) for various stocks. 


## Endpoints available

Note that currently this API wrapper does not cover all the Yahoo Finance endpoints.  In fact currently it only covers:

* Collecting the OHLC (candlestick) data for stocks on Yahoo Finance


## Getting started

Install from **PyPi** using

    pip install yahoo-finance-async

Note that you import it into your module with underscores `import yahoo_finance_async`

This library has a simple class called `OHLC` which has a simple class method (actually an async coroutine) called `fetch()` which will fetch and parse the candle (OHLC) data.

You need to `await` the response of this coroutine.

For example to fetch this historical data for the stock **AAPL**:

```python
    import asyncio

    from yahoo_finance_async import OHLC

    async def main():
        
        result = await OHLC.fetch(symbol='AAPL')
        # Do something with the result

    asyncio.run(main())
```

The returned **result** is a dictionary with two parts:

1. `candles` - these are list of candle dictionary objects.  For example:

```python
    # result['candles'] gives ...

    [
        {
            "datetime": datetime.datetime(2020, 4, 1, 0, 0),
            "open": 235.3,
            "high": 245.667,
            "low": 213.33,
            "close": 233.5,
            "volume": 23
        },
        { ... },
        { ... }
    ]
```

2. `meta` - this is the information about the symbol and timing that is returned by the Yahoo API which can be used for error checking.  For example confirming you got the right symbol and time intervals

## Additional parameters

Additional parameters can be passed to the `OHLC.fetch()` class method 

```python
    from yahoo_finance_async import OHLC, Interval, History

    # Fetch weekly candles for the last year
    await OHLC('AAPL', interval=Interval.WEEK, history=History.YEAR)

    # Fetch hourly candles for the last five days
    await OHLC('AAPL', interval=Interval.HOUR, history=History.FIVE_DAYS)
```

The `Interval` and `History` objects are Enums which show which time periods are available on the API.


## Example notebook

To see a live example you can look at the [attached notebook](examples/ohlc-example.ipynb)


## Rate limits

Be careful and kind to the Yahoo Finance API and don't hit it too hard.


## Contributing

Currently this API is focused just on the OHLC candle data.  If you wish to contribute and extend the functionality please do.  Comments, suggestions and pull requests are welcome.

Developers should clone the GitHub repo, and then install the development dependencies in the *requirement-dev.txt* file.  Run all tests with *pytest*. 

If you do contribute please also keep tests and documentation up to date.  Thanks.
