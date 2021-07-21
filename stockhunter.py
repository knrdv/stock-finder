#!/usr/bin/python3
""" Stock finder.

This program works in two ways:
	1. find risk given requested gains, stock and time window
	2. find stocks given requested gains, time window and risk tolerance
"""
import logging
import config
import argparse
import utils
import time
from collector import Collector
from daterange import DateRange
from analyzer import Analyzer
from risk_calculator import RiskCalculator
from filter import Filter

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

def main(args):
	# Using desired period, find new sample period
	start_date, end_date = DateRange(args.period, args.multiple).getRange()
	days = DateRange.periodToDays(args.period)
	
	col = Collector("yahoo", start_date, end_date)
	
	# Load tickers from file
	tickers = utils.load_tickers(args.tickers)

	if args.operation == "lookup":
		# Lookup filter
		lookup_filter = {
			"dividend":False
		}

	with open(config.CANDIDATES_FILE, "w") as f:
		pass
		
	# For each stock do:
	candidates = []
	for ticker in tickers:
		print()
		print(f"[ {ticker} analysis from {start_date} to {end_date}, gains={args.gains}%, period={args.period} ]")
		
		if args.operation == "lookup":
			utils.pprint("Applying filter...")
			
			fil = Filter(ticker).check(lookup_filter)
			if not fil:
				utils.pprint(f"Filter failed")
				continue
			utils.pprint("Filter passed")

		# Get candle OHLC data
		time.sleep(config.SLEEP)
		utils.pprint("Collecting data...")
		try:
			df = col.getData(ticker)
		except:
			print(f"Skipping {ticker}")
			continue

		# Analyze using RisingEdge analyzer
		utils.pprint(f"Starting data analysis for {ticker}...")
		try:
			an = Analyzer(args.analyzer, df, wanted_gain=args.gains, period_days=days)
		except:
			utils.pprint(f"Skipping {ticker} analysis")
			continue
		an.analyze()
		rising_edge_results = an.getResult()

		# Get averages
		an = Analyzer("avg", df)
		an.analyze()
		averages = an.getResult()

		# Analyze rolling price to rolling average ratios
		an = Analyzer("rpa", df, averages=averages["rolling_avg_price"])
		an.analyze()
		price_avg_ratios = an.getResult()

		utils.pprint("Calculating risk...")
		rc = RiskCalculator(args.analyzer, rising_edge_results)
		rc.calculateRisk()
		risk = rc.getRisk()
		utils.pprint(f"Risk: {round(risk, 2)}%")

		if risk <= args.risk_appetite:
			candidates.append(ticker)
			utils.write_candidate(ticker)

		# Calculate entry risk
		utils.pprint("Calculating entry risk...")
		input_data = {
			"ticker":ticker,
			"avg_price":averages["avg_price"],
			"rising_edge_data":rising_edge_results,
			"price_avg_ratios":price_avg_ratios
		}
		rc = RiskCalculator("per", input_data)
		rc.calculateRisk()
		risk = rc.getRisk()
		utils.pprint(f"Price entry risk: {round(risk, 2)}%")

if __name__ == "__main__":
	logging.basicConfig(format=config.LOG_FORMAT, filename=config.LOG_FILE)
	parser = argparse.ArgumentParser()
	parser.add_argument("-o", "--operation", type=str, help="operation mode", choices=["analysis", "lookup"], default="analysis")
	parser.add_argument("-t", "--tickers", type=str, help="file containing tickers", required=True)
	parser.add_argument("-a", "--analyzer", type=str, help="analyzer used", choices=["re"], required=True)
	parser.add_argument("-g", "--gains", type=int, help="\% gains", required=True)
	parser.add_argument("-r", "--risk-appetite", type=int, help="\% risk appetite", default=50)
	parser.add_argument("-p", "--period", type=str, help="max waiting period, e.g. 3w, 20d, 2m, 3y", required=True)
	parser.add_argument("-m", "--multiple", type=int, help="period multiple for sampling", required=True)
	args = parser.parse_args()
	main(args)

