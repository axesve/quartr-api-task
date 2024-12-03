import asyncio
from modules.api import AsyncSecFetcher, TickerMap
import logging

async def main():
    logging.basicConfig(level=logging.INFO)
    fetcher = AsyncSecFetcher()
    pdf_path = await fetcher.fetch_10k(TickerMap.META)
    if pdf_path:
        print(f"10-K downloaded to: {pdf_path}")
    await fetcher.close()

if __name__ == "__main__":
    asyncio.run(main())