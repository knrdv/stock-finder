#!/usr/bin/python3
import logging
import config
import argparse
import utils
#import pandas as pd
from collector import Collector
from daterange import DateRange
from analyzer import Analyzer
from risk_calculator import RiskCalculator

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

def main(args):
	#pd.set_option("display.max_columns", None)
	#pd.set_option("display.max_rows", None)

	print(f"Starting stock analysis using gains={args.gains}%, period={args.period}, multiple={args.multiple}")

	# Using desired period, find new sample period
	start_date, end_date = DateRange(args.period, args.multiple).getRange()
	days = DateRange.periodToDays(args.period)
	
	col = Collector("yahoo", start_date, end_date)
	print(f"Analysis between {start_date} and {end_date}")
	

	# Load tickers from file
	tickers = utils.load_tickers(args.tickers)

	# For each stock do:
	for ticker in tickers:
		print(f"\n##### {ticker} analysis #####")
		
		# Get candle OHLC data
		df = col.getData(ticker)

		# Analyze using RisingEdge analyzer
		an = Analyzer("re", df, wanted_gain=args.gains, period_days=days)
		an.analyze()
		results = an.getResult()
		print(results)

		rc = RiskCalculator("re", results)
		rc.calculateRisk()
		risk = rc.getRisk()

		print(f"Risk: {round(risk, 2)}%")


if __name__ == "__main__":
	logging.basicConfig(format=config.LOG_FORMAT, filename=config.LOG_FILE)
	parser = argparse.ArgumentParser()
	parser.add_argument("-t", "--tickers", type=str, help="file containing tickers", required=True)
	parser.add_argument("-g", "--gains", type=int, help="\% gains", required=True)
	parser.add_argument("-p", "--period", type=str, help="max waiting period, e.g. 3w, 20d, 2m, 3y", required=True)
	parser.add_argument("-m", "--multiple", type=int, help="period multiple for sampling", required=True)
	args = parser.parse_args()
	main(args)

