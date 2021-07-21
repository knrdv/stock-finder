import logging
import pandas
from abc import ABC, abstractmethod

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

class Analyzer:
	""" Analyzer wrapper class

	Attributes:
		atype: analyzer type
		data: data for analysis
		an: analyzer instance
	"""
	def __init__(self, atype, data, **kwargs):
		if atype == "re":
			wanted_gain = int(kwargs.pop("wanted_gain"))
			period_days = int(kwargs.pop("period_days"))
			self.an = RisingEdgeAnalyzer(data, wanted_gain, period_days)
		elif atype == "avg":
			self.an = AverageAnalyzer(data)
		elif atype == "rpa":
			averages = kwargs.pop("averages")
			self.an = RollingPriceAnalyzer(data, averages)
		else:
			loger.error("Not a reconized analyzer type")
			raise ValueError("Wrong analyzer name")

	def analyze(self):
		"""Analyze"""
		self.an.analyze()

	def getResult(self):
		"""Return analysis results"""
		return self.an.getResult()


class BaseAnalyzer(ABC):
	"""Base analyzer class used for inheritance
	
	Attributes:
		data: data for analysis
		result: analysis results
	"""
	def __init__(self, data):
		self.data = data
		self.verifyData()
		self.result = None

	@abstractmethod
	def analyze(self):
		"""Analyze data"""
		pass

	def getResult(self):
		"""Get analysis results"""
		if not self.result:
			logger.error("No results found")
			raise ValueError("No results found")
		return self.result

	@abstractmethod
	def verifyData(self):
		"""Verify required data type"""
		pass

class AverageAnalyzer(BaseAnalyzer):
	"""Average analyzer class
	
	Attributes:
		data: data for analysis
		avg_vol: average volume
		avg_price: average price
		rolling_avg_price: rolling price average
		rolling_avg_vol: rolling volume average
	"""
	def __init__(self, data):
		super().__init__(data)
		self.avg_vol = None
		self.avg_price = None
		self.rolling_avg_price = []
		self.rolling_avg_vol = []

	def calculateAverages(self):
		"""Calculate averages"""
		total_vol = 0
		total_p = 0
		ctr = 0
		for _, day in self.data.iterrows():
			total_vol += day["Volume"]
			total_p += (day["High"] + day["Low"]) / 2
			ctr += 1
			self.rolling_avg_price.append(total_p / ctr)
			self.rolling_avg_vol.append(total_vol / ctr)
		self.avg_vol = total_vol / ctr
		logger.info(f"Average volume: {self.avg_vol}")
		self.avg_price = total_p / ctr
		logger.info(f"Average price: {self.avg_price}")

	def analyze(self):
		"""Analyze data"""
		self.calculateAverages()
		self.result = {
			"avg_vol":self.avg_vol,
			"avg_price":self.avg_price,
			"rolling_avg_vol":tuple(self.rolling_avg_vol),
			"rolling_avg_price":tuple(self.rolling_avg_price)
		}

	def verifyData(self):
		"""Data type check for pandas DataFrame data"""
		datatype = type(self.data)
		if datatype is not pandas.core.frame.DataFrame:
			logger.error(f"Wrong analysis data type {datatype}")
			raise ValueError(f"Wrong analysis data type {datatype}")
		else:
			logger.info("RisingEdge analysis data type verified")


class RisingEdgeAnalyzer(BaseAnalyzer):
	""" Rising edge analyzer
	
	Finds number of rising edges of wanted gain magnitude and
	returns a tuple of possible entry points (days).

	Attributes:
		data: data to analyze
		wanted_gain: % gain wanted
		period_days: number of days in a period
	"""
	def __init__(self, data, wanted_gain, period_days):
		super().__init__(data)
		self.wanted_gain = wanted_gain
		self.period_days = period_days

	def verifyData(self):
		"""Data type check for pandas DataFrame data"""
		datatype = type(self.data)
		if datatype is not pandas.core.frame.DataFrame:
			logger.error(f"Wrong analysis data type {datatype}")
			raise ValueError(f"Wrong analysis data type {datatype}")
		else:
			logger.info("RisingEdge analysis data type verified")

	def getGains(self) -> tuple:
		"""Return % gains for each candlestick in provided data"""
		total_gains = []
		for _,day in self.data.iterrows():
			gains = day["Close"] / day["Open"]
			gains = self.getPercent(gains)
			total_gains.append(gains)
		logger.info(f"Gains:")
		logger.info(total_gains)
		return tuple(total_gains)

	def getIntTreshGain(self):
		"""Returns total occurrencies where treshold gains happened intra-day"""
		total_gains = []
		for idx, day in self.data.iterrows():
			high_sell = day["High"] / day["Open"]
			low_sell = day["Close"] / day["Low"]
			intraday_gain = max(high_sell, low_sell)
			intraday_gain = self.getPercent(intraday_gain)
			if intraday_gain >= self.wanted_gain:
				total_gains.append(int(intraday_gain // self.wanted_gain))
			else:
				total_gains.append(0)
		logger.info(f"Intraday gains:")
		logger.info(total_gains)
		return tuple(total_gains)

	def getPercent(self, gains):
		"""Returns percent"""
		if gains > 1:
			return (gains * 100) - 100
		else:
			return -1 * (1 - gains) * 100

	def countGains(self, gains:tuple, intraday:tuple=None):
		"""Calculate gains possibility for each entry point"""
		tmp_gains = [0 for _ in range(len(gains))]
		gains_counter = [0 for _ in range(len(gains))]
		for i in range(len(gains)):
			# Which gains to update
			start_idx = max(0, (i - self.period_days + 1))
			end_idx = i + 1
			for j in range(start_idx, end_idx):
				tmp_gains[j] += gains[i]
				if tmp_gains[j] >= self.wanted_gain:
					gains_counter[j] += 1
					tmp_gains[j] -= self.wanted_gain
		return tuple(gains_counter)

	def analyze(self):
		"""Main function"""
		gains_list = self.getGains()
		counted_gains = self.countGains(gains_list)
		intraday = self.getIntTreshGain()
		self.result = tuple([x + y for x,y in zip(counted_gains, intraday)])


class RollingPriceAnalyzer(BaseAnalyzer):
	"""Rolling price analyzer

	Returns tuple of open_price@date/ravg_price@date
	
	Attributes:
		data: data for analysis
		rolling_price_avgs: rolling price averages
	"""
	def __init__(self, data, rolling_price_avgs:tuple):
		super().__init__(data)
		self.averages = rolling_price_avgs
		tavg = type(self.averages)
		if tavg is not tuple:
			logger.error(f"Wrong analysis rolling_price_avgs type {tavg}")
			raise ValueError(f"Wrong analysis rolling_price_avgs type {tavg}")

	def analyze(self):
		"""Analyze data"""
		open_prices = tuple(self.data["Open"].tolist())
		tmp = [x/y for x,y in zip(open_prices, self.averages)]
		self.result = tuple(tmp)

	def verifyData(self):
		"""Data type check for pandas DataFrame data"""
		datatype = type(self.data)
		if datatype is not pandas.core.frame.DataFrame:
			logger.error(f"Wrong analysis data type {datatype}")
			raise ValueError(f"Wrong analysis data type {datatype}")
		else:
			logger.info("RollingPriceAnalyzer analysis data type verified")