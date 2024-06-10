from earnings_calls_src import get_earnings_all_docs
from filings_src import sec_main as unstructured_sec_main
from marker_sec_src.sec_filings_to_pdf import sec_save_pdfs
from marker_sec_src.pdf_to_md import run_marker as run_marker_single
from marker_sec_src.pdf_to_md_parallel import run_marker_parallel
from typing import List, Optional

def get_data(
        ticker:str,
        year:str,
        filing_types:List[str] = ["10-K", "10-Q"],
        data_sources:List[str] = ['unstructured'],
        include_amends=True,
        batch_processing:bool=False,
        batch_multiplier:Optional[int]=None,
        workers:Optional[int] = None,
        inference_ram:Optional[int] = None,
        vram_per_task:Optional[int] = None,
        num_chunks:Optional[int] = None,
):
    
    for ds in data_sources:
        assert ds in ['unstructured','earnings_calls','marker_pdf'], "The valid data sources are ['unstructured','earnings_calls','marker_pdf']"
    if 'marker_pdf' in data_sources:
        html_urls, metadata_json, input_ticker_year_path = sec_save_pdfs(
            ticker, year, filing_types, include_amends
        )
        if not batch_processing:
            assert batch_multiplier is not None, "The batch multiplier is not specified"
            run_marker_single(
            input_ticker_year_path=input_ticker_year_path,
            ticker=ticker,
            year=year,
            batch_multiplier=batch_multiplier,
        )
        elif batch_processing:
            run_marker_parallel(
                input_ticker_year_path=input_ticker_year_path,
                ticker=ticker,
                year=year,
                workers=workers,
                inference_ram=inference_ram,
                vram_per_task=vram_per_task,
                num_chunks=num_chunks,
                batch_multiplier=batch_multiplier,
            )
    elif 'unstructured' in data_sources:
        sec_data,sec_form_names = unstructured_sec_main(ticker,year,filing_types,include_amends)
        return sec_data,sec_form_names
    elif 'earnings_calls' in data_sources:
        earnings_docs,earnings_call_quarter_vals,speakers_list_1,speakers_list_2,speakers_list_3,speakers_list_4 = get_earnings_all_docs(ticker,year)
        return (
            earnings_docs,
            earnings_call_quarter_vals,
            speakers_list_1,
            speakers_list_2,
            speakers_list_3,
            speakers_list_4,
        )


