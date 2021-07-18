import logging
import yfinance as yf

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

class Filter():
	"""Filter class
	
	This class implements a filter based on various ticker attributes.
	"""
	def __init__(self, ticker):
		self.ticker = yf.Ticker(ticker)

	def eq(self, s, val):
		return s == val

	def ne(self, s, val):
		return not s == val

	def gt(self, s, val):
		return s > val

	def lt(self, s, val):
		return s < val

	def gte(self, s, val):
		return s >= val

	def lte(self, s, val):
		return s <= val

	def dividend(self, exists):
		"""Dividend check"""
		div = self.ticker.info["dividendRate"]
		if not div:
			empty = True
		else:
			empty = (len(div) == 0)
		divcheck = (empty != exists)
		if divcheck:
			logger.info("Dividend check passed")
		else:
			logger.info("Dividend check failed")
		return empty != exists

	def volume(self, j_fil):
		"""Volume check loop"""
		vol = self.ticker.info["volume"]
		passed = True
		for key, val in j_fil.items():
			result = getattr(self, key)(vol, val)
			passed = passed and result
			if not passed:
				logger.info("Volume check failed")
				return False
		logger.info("Volume check passed")
		return passed

	def check(self, j_fil):
		"""Main check loop"""
		passed = True
		for key, val in j_fil.items():
			result = getattr(self, key)(val)
			passed = passed and result
			if not passed:
				logger.info("Global check failed")
				return False
		logger.info("Filter passed")
		return passed