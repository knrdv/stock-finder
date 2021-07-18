import logging
from abc import ABC, abstractmethod

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

class RiskCalculator:
	""" Wrapper class

	This class is a wrapper for all used risk calculators.
	Attributes:
		rc: chosen risk calculator by given type
		analysis_data: data given by analyzer
	"""
	def __init__(self, rtype, analysis_data):
		if rtype == "re":
			self.rc = RERiskCalculator(analysis_data)
			logger.info("Loaded rising edge risk calculator")
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
		self.verifyData()
		self.risk = None

	@abstractmethod
	def calculateRisk(self):
		"""Calculate risk"""
		pass

	@abstractmethod
	def getRisk(self):
		"""Return calculated risk"""
		pass

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

	def calculateRisk(self):
		"""Calculate risk by finding fails frequency"""
		failed = sum(x == 0 for x in self.analysis_data)
		self.risk = (failed / len(self.analysis_data)) * 100

	def getRisk(self):
		if not self.risk:
			logger.error("No risk calculated")
			raise ValueError("No risk calculated")
		return self.risk

	def verifyData(self):
		"""Check if provided data is in tuple"""
		datatype = type(self.analysis_data)
		if datatype is not tuple:
			logger.error(f"Wrong analysis data type {datatype}")
			raise ValueError(f"Wrong analysis data type {datatype}")
		else:
			logger.info("RisingEdge data type verified")