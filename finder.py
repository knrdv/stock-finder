#!/usr/bin/python3
import logging
import config
import argparse
import utils
import pandas as pd

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

def main(args):
	pd.set_option("display.max_columns", None)
	pd.set_option("display.max_rows", None)

	print(f"Starting stock analysis using gains={args.gains}%, period={args.period}, multiple={args.multiple}")

	# Using desired period, find new sample period
	end_date = utils.get_current_date()
	start_date = utils.get_starting_date(args.period, args.multiple)
	days = utils.period_to_days(args.period)
	print(f"Analysis between {start_date} and {end_date}")

	# Load tickers
	tickers = utils.load_tickers(args.tickers)

	# For each stock do:
	for ticker in tickers:
		print(f"\n##### {ticker} analysis #####")
		# Get candles in sample period with 1day/candle
		df = utils.download_ticker_data(ticker, start_date, end_date)

		# Get list/tuple of gains for each day
		gains_list = utils.get_gains(df)
		
		# Find how many occurrences of %gains were in sample period
		gains_info = utils.count_gains(gains_list, args.gains, days)

		#print(f"Entry points at which {args.gains}% gains would be fulfilled inside period of {args.period}")
		#print(gains_info)
		elements = sum(x > 0 for x in gains_info)
		print(f"Positive entry points: {elements}")
		
		# Calculate risk as number of failed entry points
		result = utils.calculate_risk(gains_info)
		print(f"Risk: {round(result, 2)}%")


if __name__ == "__main__":
	logging.basicConfig(format=config.LOG_FORMAT, filename=config.LOG_FILE)
	parser = argparse.ArgumentParser()
	parser.add_argument("-t", "--tickers", type=str, help="file containing tickers", required=True)
	parser.add_argument("-g", "--gains", type=int, help="\% gains", required=True)
	parser.add_argument("-p", "--period", type=str, help="max waiting period, e.g. 3w, 20d, 2m, 3y", required=True)
	parser.add_argument("-m", "--multiple", type=int, help="period multiple for sampling", required=True)
	args = parser.parse_args()
	main(args)

