from sec_edgar_downloader import Downloader

from secedgar import filings, FilingType

# 10Q filings for Apple and Facebook (tickers "aapl" and "fb")
my_filings = filings(cik_lookup=["aapl", "fb"],
                     filing_type=FilingType.FILING_10Q,
                     user_agent="arnavraj0015@gmail.com")
my_filings.save('/home/arnav/Documents/intern/georgia_tech')