from marker_src.sec_filings_to_pdf import sec_save_pdfs
from marker_src.pdf_to_md import run_marker
import argparse

parser = argparse.ArgumentParser(
                    prog='Marker SEC Filings PDF to MD',
                    description='It converts SEC filings from PDF to MD')

parser.add_argument('-t','--ticker', type=str, help='Ticker of the company')
parser.add_argument('-y','--year', type=str, help='Year of the filings')
parser.add_argument('-ia','--include_amends',type=str, help="Whether to include amendment files")
parser.add_argument('-ft','--filing_types',type=str,help="Filings types separated by commas")
# parser.add_argument("--num_chunks", type=int, default=1, help="Number of chunks being processed in parallel")
# parser.add_argument("--max", type=int, default=None, help="Maximum number of pdfs to convert")
# parser.add_argument("--workers", type=int, default=5, help="Number of worker processes to use")
parser.add_argument("-bm","--batch_multiplier", type=int, default=2,help="Number of pages to process")

args = parser.parse_args()

assert args.include_amends in ["true", "false"], "The include_amends argument is either true or false"
filings_types_list = args.filing_types.split(",")
include_amends = True if args.include_amends == "true" else False


html_urls, metadata_json, input_ticker_year_path = sec_save_pdfs(args.ticker,args.year,filings_types_list,include_amends)
print("Saved files, Now converting to markdowns")
run_marker(
    input_ticker_year_path=input_ticker_year_path,
    ticker=args.ticker,
    year=args.year,
    # workers=args.workers,
    # max_workers=args.max,
    # num_chunks=args.num_chunks,
    batch_multiplier=args.batch_multiplier,
)
print("Done converting")