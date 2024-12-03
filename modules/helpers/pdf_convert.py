import os
import aiofiles
import logging
from typing import Optional

import pdfkit
PATH_TO_WKHTMLTOPDF = r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe'

config = pdfkit.configuration(wkhtmltopdf=PATH_TO_WKHTMLTOPDF)

class AsyncPDFConverter:
    def __init__(self, 
                 base_storage_path: str = 'storage/pdf',
                 logger: Optional[logging.Logger] = None):
        self.base_storage_path = base_storage_path
        self.logger = logger or logging.getLogger(__name__)

    async def save_pdf(self, ticker: str, filing_date: str, filing_url: str) -> str:
        """
        Asynchronously save the HTML content as a PDF under year/ticker/ directory structure.
        """
        year = filing_date[:4]

        year_directory = os.path.join(self.base_storage_path, year)
        ticker_directory = os.path.join(year_directory, ticker)
        
        os.makedirs(ticker_directory, exist_ok=True)

        pdf_filename = f"{ticker}-{filing_date}_10k.pdf"
        pdf_file_path = os.path.join(ticker_directory, pdf_filename)

        try:
            pdfkit.from_url(url=filing_url, output_path=pdf_file_path, configuration=config)
            
            self.logger.info(f"PDF saved at {pdf_file_path}")
            return pdf_file_path
        except Exception as e:
            self.logger.error(f"Error saving PDF: {e}")
            raise

    async def fetch_and_save_10k(self, ticker_name: str, filing_url: str, date: str) -> str:
        """
        Asynchronously fetch the HTML from the SEC filing URL and save it as a PDF.
        """
        return await self.save_pdf(ticker_name, date, filing_url)