import yfinance as yf
import logging
from abc import ABC, abstractmethod

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class Collector:
	def __init__(self, ctype, start_date, end_date):
		if ctype == "yahoo":
			self.col = YahooCollector(start_date, end_date)
			logger.info("initialized yahoo collector")
		else:
			logger.error("Unvalid collector type provided")
			raise ValueError("Unvalid collector type")

	def getData(self, ticker):
		return self.col.getCandleData(ticker)


class BaseCollector(ABC):
	def __init__(self, start_date, end_date):
		self.start_date = start_date
		self.end_date = end_date

	@abstractmethod
	def getCandleData(self, ticker):
		pass


class YahooCollector(BaseCollector):
	def __init__(self, start_date, end_date):
		super().__init__(start_date, end_date)

	def getCandleData(self, ticker):
		logger.info(f"fetching data for {ticker} starting {self.start_date} ending {self.end_date}")
		data = yf.download(ticker, start=self.start_date, end=self.end_date)
		return data
