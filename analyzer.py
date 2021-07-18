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
			print("wanted gain:", wanted_gain)
			self.an = RisingEdgeAnalyzer(data, wanted_gain, period_days)
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

	@abstractmethod
	def getResult(self):
		"""Get analysis results"""
		pass

	@abstractmethod
	def verifyData(self):
		"""Verify required data type"""
		pass

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

	def getGains(self):
		"""Return % gains for each candlestick in provided data"""
		total_gains = []
		for _,day in self.data.iterrows():
			gains = day["Close"] / day["Open"]
			gains = self.getPercent(gains)
			total_gains.append(gains)
		return tuple(total_gains)

	def getPercent(self, gains):
		"""Returns percent"""
		if gains > 1:
			return (gains * 100) - 100
		else:
			return -1 * (1 - gains) * 100

	def countGains(self, gains):
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
		self.result = self.countGains(gains_list)

	def getResult(self):
		"""Return analysis results"""
		if not self.result:
			logger.error("No results found")
			raise ValueError("No results found")
		return self.result