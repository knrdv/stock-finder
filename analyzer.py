import logging
from abc import ABC, abstractmethod

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class Analyzer:
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
		self.an.analyze()

	def getResult(self):
		return self.an.getResult()

class BaseAnalyzer(ABC):
	def __init__(self, data):
		self.data = data
		self.result = None

	@abstractmethod
	def analyze(self):
		pass

	@abstractmethod
	def getResult(self):
		pass

class RisingEdgeAnalyzer(BaseAnalyzer):
	def __init__(self, data, wanted_gain, period_days):
		super().__init__(data)
		self.wanted_gain = wanted_gain
		self.period_days = period_days

	def getGains(self):
		total_gains = []
		for _,day in self.data.iterrows():
			gains = day["Close"] / day["Open"]
			gains = self.getPercent(gains)
			total_gains.append(gains)
		return tuple(total_gains)

	def getPercent(self, gains):
		if gains > 1:
			return (gains * 100) - 100
		else:
			return -1 * (1 - gains) * 100

	def countGains(self, gains):
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
		gains_list = self.getGains()
		self.result = self.countGains(gains_list)

	def getResult(self):
		if not self.result:
			logger.error("No results found")
			raise ValueError("No results found")
		return self.result