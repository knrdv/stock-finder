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

	def primitiveFilter(self, tested_val, j_fil):
		"""Test through primitive filters"""
		passed = True
		for key, val in j_fil.items():
			result = getattr(self, key)(tested_val, val)
			passed = passed and result
			if not passed:
				logger.info(f"Primitive check {key} failed")
				return False
		logger.info(f"Primitive check {key} passed")
		return passed

	def dividend(self, wanted_div):
		"""Dividend check"""
		try:
			div = self.ticker.info["dividendRate"]
		except:
			div = None
		print(div)
		if not div:
			has_div = False
		else:
			has_div = True
		divcheck = not (has_div ^ wanted_div)
		if divcheck:
			logger.info("Dividend check passed")
		else:
			logger.info("Dividend check failed")
		return divcheck

	def volume(self, j_fil):
		"""Volume check loop"""
		vol = self.ticker.info["volume"]
		logger.info(f"Volume: {vol}")
		ret = self.primitiveFilter(vol, j_fil)
		if ret:
			logger.info("Volume check passed")
		else:
			logger.info("Volume check failed")
		return ret

	def marketcap(self, j_fil):
		"""Volume check loop"""
		mcap = self.ticker.info["marketCap"]
		logger.info(f"Market cap: {mcap}")
		ret = self.primitiveFilter(mcap, j_fil)
		if ret:
			logger.info("Market cap check passed")
		else:
			logger.info("Market cap check failed")
		return ret

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