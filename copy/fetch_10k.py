import os
from datetime import datetime
from sec_edgar_downloader import Downloader
import argparse

def download_10k_filings(company_name, email_address, ticker, start_year=None, end_year=None):
    """Download 10-K filings using sec_edgar_downloader, handling exceptions and improving feedback."""
    data_dir = os.path.join(os.getcwd(), "data", "sec-edgar-filings", ticker)
    os.makedirs(data_dir, exist_ok=True)
    
    # Initialize the Downloader to the specified directory
    dl = Downloader(company_name, email_address, os.path.join(os.getcwd(), data_dir))

    # Handling start and end years
    if start_year:
        start_date = datetime(start_year, 1, 1)
    else:
        start_date = datetime(1995, 1, 1)  # Assuming 1995 as a default start year

    if end_year:
        end_date = datetime(end_year, 12, 31)
    else:
        end_date = datetime.now()  # Defaults to current date

    try:
        # Download the 10-K filings from the specified date range
        num_filings = dl.get("10-K", ticker, after=start_date, before=end_date, include_amends=False)
        print(f"Downloaded {num_filings} 10-K filings for {ticker} from {start_year if start_year else 'earliest available'} to {end_year if end_year else 'current year'}.")
    except Exception as e:
        print(f"Error downloading 10-K filings for {ticker}: {e}")
        raise RuntimeError(f"Failed to download 10-K filings due to: {e}")

def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description="Download 10-K filings for a company")
    parser.add_argument("--company", type=str, help="The company name")
    parser.add_argument("--email", type=str, help="The email address")
    parser.add_argument("--ticker", type=str, help="The company ticker")
    parser.add_argument("--start_year", type=int, help="The start year")
    parser.add_argument("--end_year", type=int, help="The end year")
    return parser.parse_args()

if __name__ == "__main__":
    args = parse_args()
    download_10k_filings(args.company, args.email, args.ticker, args.start_year, args.end_year)