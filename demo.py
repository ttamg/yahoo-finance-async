import asyncio
from yahoo_finance import OHLC


async def main():
    output = await OHLC.fetch(symbol="AAPL")
    print(output)


asyncio.run(main())