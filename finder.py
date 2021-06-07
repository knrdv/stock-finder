#!/usr/bin/python3
import logging
import yfinance as yf
import pandas as pd
import config
import argparse
import json
from collector import Collector

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

def load_tickers(filename):
	tickers = []
	with open(args.tickers, "r") as f:
		for ticker in f.readlines():
			tickers.append(ticker.strip())
	return tuple(tickers)

def pretty(ticker):
	return json.dumps(ticker, indent=4)

def main(args):

	pd.set_option("display.max_columns", None)
	tickers = load_tickers(args.tickers)

	col = Collector()

	for ticker in tickers:
		print(pretty(col.getInfo(ticker)))


if __name__ == "__main__":
	logging.basicConfig(format=config.LOG_FORMAT, filename=config.LOG_FILE)
	parser = argparse.ArgumentParser()
	parser.add_argument("tickers", type=str, help="file containing tickers")
	#parser.add_argument("-o", "--output", help="output file")
	args = parser.parse_args()
	main(args)

