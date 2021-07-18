import json
import logging
import datetime
import yfinance as yf
import pandas as pd
import functools
from collections import Counter

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

def load_tickers(filename:str) -> tuple:
	"""Load tickers from file to tuple"""
	tickers = []
	with open(filename, "r") as f:
		for ticker in f.readlines():
			tickers.append(ticker.strip())
	return tuple(tickers)

def date_to_str(date):
	"""Format datetime date to string"""
	ret = date.strftime("%Y-%m-%d")
	return ret

def pprint(msg):
	print(f"[+] {msg}")