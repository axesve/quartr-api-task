# Quartr SEC 10-K Filing Fetcher

A Python-based asynchronous tool for downloading 10-K filings from the SEC EDGAR database for specified company tickers.

## Prerequisites & Dependencies

This project requires Python 3.8+ and the following packages:

- `aiohttp` - Asynchronous HTTP client
- `aiofiles` - Asynchronous file I/O
- `pdfkit` - A Python wrapper for wkhtmltopdf (converts HTML to PDF)
- `wkhtmltopdf` - A command-line tool to render HTML to PDF

## Installation

#### Clone the repository:

#### git clone https://github.com/axesve/quartr-api-task.git
#### cd quartr-api-task

# Install Python dependencies:

#### pip install -r requirements.txt

# Install wkhtmltopdf:

#### macOS: brew install Caskroom/cask/wkhtmltopdf
#### Windows: choco install wkhtmltopdf
#### Linux: apt-get install wkhtmltopdf

#### Update PATH_TO_WKHTMLTOPDF in modules/helpers/pdf_convert.py with your installation path

## Usage

#### in the root of quartr-api-task run
#### python main.py
```python
import asyncio
from modules.api import AsyncSecFetcher, TickerMap
import logging

async def main():
    logging.basicConfig(level=logging.INFO)
    fetcher = AsyncSecFetcher()
    pdf_path = await fetcher.fetch_10k(TickerMap.AAPL)
    if pdf_path:
        print(f"10-K downloaded to: {pdf_path}")
    await fetcher.close()

if __name__ == "__main__":
    asyncio.run(main())
```