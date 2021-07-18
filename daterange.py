import logging
import datetime

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

class DateRange:
	def __init__(self, period, multiple=1):
		self.period = period
		self.multiple = multiple
		self.start_date = self.getStartDate()
		self.end_date = self.getEndDate()

	@staticmethod
	def periodToDays(period):
		logger.info(f"translating {period} to days")
		label = period[-1]
		num = int(period[:-1])
		multiplier = 1

		if label == "w":
			multiplier = 7
		elif label == "m":
			multiplier = 30
		elif label == "y":
			multiplier = 365

		days_num = num * multiplier
		logger.info(f"{period} is {days_num} days")
		return days_num

	@staticmethod
	def getCurrentDate():
		return datetime.date.today()

	def getStartDate(self):
		logger.info(f"finding starting date for period {self.period}")
		curr = DateRange.getCurrentDate()
		days = DateRange.periodToDays(self.period)
		one_day = datetime.timedelta(days=1)
		start_date = curr - self.multiple * days * one_day
		logger.info(f"starting date is {start_date}")
		return start_date

	def getEndDate(self):
		return DateRange.getCurrentDate()

	def getRange(self):
		if not self.start_date or not self.end_date:
			logger.error("No start or end date to return")
			raise ValueError("No start or end date")
		return (self.start_date, self.end_date)