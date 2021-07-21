import yfinance as yf
import logging
from abc import ABC, abstractmethod, abstractstaticmethod

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

class Collector:
	""" Collector wrapper class
	
	Collects data from a certain source.

	Attributes:
		ctype: collector type
		start_date: start date
		end_date: end date
		col: collector instance
	"""
	def __init__(self, ctype, start_date, end_date):
		if ctype == "yahoo":
			self.col = YahooCollector(start_date, end_date)
			logger.info("initialized yahoo collector")
		else:
			logger.error("Unvalid collector type provided")
			raise ValueError("Unvalid collector type")

	def getData(self, ticker):
		"""Returns OHLC candle data for a given ticker"""
		return self.col.getCandleData(ticker)


class BaseCollector(ABC):
	"""Collector base class for inheritance

	Attributes:
		start_date: start date
		end_date: end date
	"""
	def __init__(self, start_date, end_date):
		self.start_date = start_date
		self.end_date = end_date

	@abstractstaticmethod
	def getPrice(ticker):
		pass

	@abstractstaticmethod
	def getVolume(ticker):
		pass

	@abstractmethod
	def getCandleData(self, ticker):
		"""Get candle data in given period for a given ticker"""
		pass


class YahooCollector(BaseCollector):
	"""Yahoo collector

	Collect candlestick data using yahoo finance API
	"""
	def __init__(self, start_date, end_date):
		super().__init__(start_date, end_date)

	def getCandleData(self, ticker):
		logger.info(f"fetching data for {ticker} starting {self.start_date} ending {self.end_date}")
		data = yf.download(ticker, start=self.start_date, end=self.end_date)
		return data

	@staticmethod
	def getPrice(ticker) -> int:
		data = yf.Ticker(ticker)
		price = int(data.info["currentPrice"])
		return price

	@staticmethod
	def getVolume(ticker) -> int:
		data = yf.Ticker(ticker)
		vol = int(data.info["volume"])
		return vol
