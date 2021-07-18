import json
import logging
import datetime
import yfinance as yf
import pandas as pd
import functools
from collections import Counter

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

def load_tickers(filename):
	tickers = []
	with open(filename, "r") as f:
		for ticker in f.readlines():
			tickers.append(ticker.strip())
	return tuple(tickers)

def pretty(ticker):
	return json.dumps(ticker, indent=4)

def date_to_str(date):
	ret = date.strftime("%Y-%m-%d")
	return ret

def get_percent(gains):
	if gains > 1:
		return (gains * 100) - 100
	else:
		return -1 * (1 - gains) * 100

def get_gains(df) -> tuple:
	total_gains = []
	for _,day in df.iterrows():
		gains = day["Close"] / day["Open"]
		gains = get_percent(gains)
		total_gains.append(gains)
	return tuple(total_gains)

# Return number of ocurrencies of gains
def count_gains(gains:tuple, wanted_gain:int, period):
	tmp_gains = [0 for _ in range(len(gains))]
	gains_counter = [0 for _ in range(len(gains))]
	for i in range(len(gains)):
		# Which gains to update
		start_idx = max(0, (i-period+1))
		end_idx = i+1
		for j in range(start_idx, end_idx):
			tmp_gains[j] += gains[i]
			if tmp_gains[j] >= wanted_gain:
				gains_counter[j] += 1
				tmp_gains[j] -= wanted_gain
	return tuple(gains_counter)

def calculate_risk(entrypoints:tuple):
	failed = sum(x == 0 for x in entrypoints)
	result = (failed / len(entrypoints)) * 100
	return result