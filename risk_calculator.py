import logging
from abc import ABC, abstractmethod
from collector import YahooCollector

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

class RiskCalculator:
	""" Wrapper class

	This class is a wrapper for all used risk calculators.
	Attributes:
		rc: chosen risk calculator by given type
		analysis_data: data given by analyzer
	"""
	def __init__(self, rtype, analysis_data, **kwargs):
		if rtype == "re":
			self.rc = RERiskCalculator(analysis_data)
			logger.info("Loaded rising edge risk calculator")
		elif rtype == "per":
			self.rc = PriceEntryRiskCalculator(analysis_data)
		else:
			logger.error("Wrong risk calculator type")
			raise ValueError("Wrong risk calculator type")
	
	def calculateRisk(self):
		"""Risk calculation wrapper"""
		self.rc.calculateRisk()

	def getRisk(self):
		"""Return calculated risk"""
		return self.rc.getRisk()


class BaseRiskCalculator(ABC):
	""" Risk calculator base class

	Attributes:
		analysis_data: analyzer data
		risk: risk percent calculated
	"""
	def __init__(self, analysis_data):
		self.analysis_data = analysis_data
		self.risk = None

	@abstractmethod
	def calculateRisk(self):
		"""Calculate risk"""
		pass

	def getRisk(self):
		"""Return calculated risk"""
		if not self.risk:
			logger.error("No risk calculated")
			raise ValueError("No risk calculated")
		return self.risk

	@abstractmethod
	def verifyData(self):
		"""Verify that the data provided is suitable for type of risk calculator"""
		pass

class RERiskCalculator(BaseRiskCalculator):
	""" Rising edge risk calculator

	Calculates risk based on data given by rising edge analyzer.
	Attributes:
		analysis_data: tuple of entry points
	"""
	def __init__(self, analysis_data):
		super().__init__(analysis_data)
		self.verifyData()

	def calculateRisk(self):
		"""Calculate risk by finding fails frequency"""
		failed = sum(x == 0 for x in self.analysis_data)
		self.risk = (failed / len(self.analysis_data)) * 100

	def verifyData(self):
		"""Check if provided data is in tuple"""
		datatype = type(self.analysis_data)
		if datatype is not tuple:
			logger.error(f"Wrong analysis data type {datatype}")
			raise ValueError(f"Wrong analysis data type {datatype}")
		else:
			logger.info("RisingEdge data type verified")


class PriceEntryRiskCalculator(BaseRiskCalculator):
	"""Complex Rising edge risk calculator

	Calculates risk based on data given by rising edge analyzer and price to rolling average ratios
	Attributes:
		analysis_data: 
			{
				"ticker":ticker,
				"avg_price":averages["avg_price"],
				"rising_edge_data":rising_edge_results,
				"price_avg_ratios":price_avg_ratios
			}
	"""
	def __init__(self, analysis_data:dict):
		super().__init__(analysis_data)
		self.verifyData()

	def calculateRisk(self):
		"""Calculate price entry risk"""
		
		# Get current price
		current_price = YahooCollector.getPrice(self.analysis_data["ticker"])

		# Get average price as last rolling average price
		average_price = self.analysis_data["avg_price"]

		current_price_ratio = current_price / average_price
		#print("Current price/avg ratio:", current_price_ratio, average_price)

		rising_edge_data = self.analysis_data["rising_edge_data"]
		price_avg_ratios = self.analysis_data["price_avg_ratios"]

		total_ratios = 0
		counter = 0
		for i in range(len(rising_edge_data)):
			if rising_edge_data[i] > 0:
				counter += rising_edge_data[i]
				total_ratios += price_avg_ratios[i]*rising_edge_data[i]

		average_win_ratio = total_ratios / counter
		#print("Average win ratio:", average_win_ratio)

		# Where we stand
		#similarity = current_price_ratio / average_win_ratio
		if current_price_ratio >= 1:
			self.risk = 100
		elif current_price_ratio < average_win_ratio:
			self.risk = 0
		else:
			self.risk = (current_price_ratio - average_win_ratio)/(1 - average_win_ratio)*100 


	def verifyData(self):
		"""Check if provided data is in tuple"""
		datatype = type(self.analysis_data)
		if datatype is not dict:
			logger.error(f"Wrong analysis data type {datatype}")
			raise ValueError(f"Wrong analysis data type {datatype}")
		else:
			logger.info("RisingEdge data type verified")