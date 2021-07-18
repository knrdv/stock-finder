import logging
from abc import ABC, abstractmethod

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class RiskCalculator:
	def __init__(self, rtype, analysis_data):
		if rtype == "re":
			self.rc = RERiskCalculator(analysis_data)
		else:
			logger.error("Wrong risk calculator type")
			raise ValueError("Wrong risk calculator type")
	
	def calculateRisk(self):
		self.rc.calculateRisk()

	def getRisk(self):
		return self.rc.getRisk()

class BaseRiskCalculator(ABC):
	def __init__(self, analysis_data):
		self.analysis_data = analysis_data
		self.risk = None

	@abstractmethod
	def calculateRisk(self):
		pass

	@abstractmethod
	def getRisk(self):
		pass

class RERiskCalculator(BaseRiskCalculator):
	def __init__(self, analysis_data):
		super().__init__(analysis_data)

	def calculateRisk(self):
		failed = sum(x == 0 for x in self.analysis_data)
		self.risk = (failed / len(self.analysis_data)) * 100
		elements = sum(x > 0 for x in self.analysis_data)
		print(f"Positive entry points: {elements}")

	def getRisk(self):
		if not self.risk:
			logger.error("No risk calculated")
			raise ValueError("No risk calculated")
		return self.risk