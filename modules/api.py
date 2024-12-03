import aiohttp
import logging
from enum import StrEnum
from typing import Optional, Dict, Any

from modules.helpers.pdf_convert import AsyncPDFConverter

class TickerMap(StrEnum):
    """
    Please be advised, this is not a complete list.
    """
    AAPL = "0000320193"
    META = "0001326801"
    GOOGL = "0001652044"
    AMZN = "0001018724"
    NFLX = "0001065280"
    GS = "0000886982"

class AsyncSecFetcher:
    BASE_URL = "https://data.sec.gov"
    USER_AGENT = "qartr_fetcher/1.0 (axel.svensson@quartr.com)"
    def __init__(self, logger: Optional[logging.Logger] = None):
        self.logger = logger or logging.getLogger(__name__)
        self.session = aiohttp.ClientSession(
            headers={"User-Agent": self.USER_AGENT}
        )
        self.pdf_converter = AsyncPDFConverter()

    async def fetch_submissions(self, ticker: TickerMap) -> Dict[str, Any]:
        """
        Asynchronously fetches the submission data for a given ticker.
        """
        if not self.session:
            raise RuntimeError("Session not initialized. Use async context manager.")

        url = f"{self.BASE_URL}/submissions/CIK{ticker.value}.json"
        self.logger.info(f"Fetching submissions for {ticker.name} (CIK: {ticker.value})")

        async with self.session.get(url) as response:
            if response.status == 200:
                return await response.json()
            else:
                raise ValueError(f"Unable to fetch submissions for {ticker.name}. Response: {response.status}")

    async def fetch_10k(self, ticker: TickerMap) -> Optional[str]:
        submissions = await self.fetch_submissions(ticker)
        
        filings = submissions.get("filings", {}).get("recent", {})
        if not filings:
            self.logger.warning(f"No recent filings found for {ticker.name}")
            return None

        # Find the most recent 10-K filing
        for form, url, date, acc_num in sorted(
            zip(
                filings.get("form", []), 
                filings.get("primaryDocument", []), 
                filings.get("filingDate", []),
                filings.get("accessionNumber", [])
            ), 
            key=lambda x: x[2], 
            reverse=True
        ):
            if form == "10-K":
                acc_num_clean = acc_num.replace("-", "")
                filing_url = f"https://www.sec.gov/Archives/edgar/data/{ticker.value}/{acc_num_clean}/{url}"
                
                try:
                    return await self.pdf_converter.save_pdf(ticker.name, date, filing_url)
                except Exception as e:
                    self.logger.warning(f"Failed to fetch 10-K for {ticker.name} from {filing_url}: {e}")
                    break

        return None
    
    async def close(self) -> None:
        await self.session.close()