import yfinance as yf

class Collector:

	def __init__(self, ticker):
		self.data = yf.Ticker(ticker)

	def getInfo(self):
		"""
		Interesting self.data:
			fullTimeEmployees
			industry
			previousClose
			regularMarketOpen
			twoHundredDayAverage
			regularMarketDayHigh
			averageDailyVolume10Day
			regularMarketPreviousClose
			fiftyDayAverage
			open
			averageVolume10days
			beta
			regularMarketDayLow
			regularMarketVolume
			marketCap
			averageVolume
			priceToSalesTrailing12Months
			dayLow
			volume
			fiftyTwoWeekHigh
			forwardPE
			fiftyTwoWeekLow
			dayHigh
			enterpriseToRevenue
			profitMargins
			enterpriseToEbitda
			forwardEps
			52WeekChange
			sharesOutstanding
			bookValue
			sharesShort
			sharesPercentSharesOut
			heldPercentInstitutions
			netIncomeToCommon
			trailingEps
			priceToBook
			heldPercentInsiders
			nextFiscalYearEnd
			mostRecentQuarter
			shortRatio
			sharesShortPreviousMonthDate
			floatShares
			enterpriseValue
			earningsQuarterlyGrowth
			dateShortInterest
			shortPercentOfFloat
			sharesShortPriorMonth
			regularMarketPrice
		"""
		return self.data.info

	def getHistory(self, period):
		return self.data.history(period=period)

	def getDividends(self):
		return self.data.dividends

	def getSplits(self):
		return self.data.splits

	def getFinancials(self):
		return self.data.financials

	def getFinancialsQ(self):
		return self.data.quarterly_financials

	def getMajorHolders(self):
		return self.data.major_holders

	def getInstitutionalHolders(self):
		return self.data.insitutional_holders

	def getBalanceSheet(self):
		return self.data.balance_sheet

	def getBalanceSheetQ(self):
		return self.data.quarterly_balance_sheet

	def getCashflow(self):
		return self.data.cashflow

	def getCashflowQ(self):
		return self.data.quarterly_cashflow

	def getEarnings(self):
		return self.data.earnings

	def getEarningsQ(self):
		return self.data.quarterly_earnings

	def getCalendar(self):
		return self.data.calendar