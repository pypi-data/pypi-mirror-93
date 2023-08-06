import maglev
import carloancalculator

from typing import Any, List, Callable

class CarLoanCalculator:
	"""
	car loan
	calculator
	"""
	def __init__(self):
		bus = maglev.maglev_MagLev.getInstance("default")
		lib = carloancalculator.carloancalculator_CarLoanCalculator(bus)

	def CalcPayments(self, newCarPrice: float, tradeInAllowance: float, tradeInLoanBalance: float, downPaymentAndRebates: float, loanDuration: float, salesTaxRate: float, interestRate: float) -> List[Any]:
		"""		Calculate what the payments would be from the price of the new car and the parameters of the monthly loan payments
		Args:
			newCarPrice (float):price of the car new
			tradeInAllowance (float):trade-in value
			tradeInLoanBalance (float):loan balance after trade-in
			downPaymentAndRebates (float):total amount of rebates plus downpayment
			loanDuration (float):loan duration in months
			salesTaxRate (float): sales tax as percentage
			interestRate (float):interest rate as percentage
		Returns:
			payments and total interest
		"""
		pybus = maglev.maglev_MagLevPy.getInstance("default")
		args = [newCarPrice, tradeInAllowance, tradeInLoanBalance, downPaymentAndRebates, loanDuration, salesTaxRate, interestRate]
		ret = None
		def CalcPayments_Ret(async_ret):
			nonlocal ret
			ret = async_ret
		pybus.call('CarLoanCalculator.CalcPayments', args, CalcPayments_Ret)
		return ret

	def CalcAffordability(self, monthlyPayment: float, tradeInAllowance: float, tradeInLoanBalance: float, downPaymentAndRebates: float, loanDuration: float, salesTaxRate: float, interestRate: float) -> float:
		"""		Calculate the price of the car from the monthly loan payment information
		Args:
			monthlyPayment (float):monthly payment amount
			tradeInAllowance (float):trade-in value
			tradeInLoanBalance (float):loan balance after trade-in
			downPaymentAndRebates (float):total amount of rebates plus downpayment
			loanDuration (float):loan duration in months
			salesTaxRate (float):sales tax rate as percentage
			interestRate (float):interest rate as percentage
		Returns:
			target price with tax and fees
		"""
		pybus = maglev.maglev_MagLevPy.getInstance("default")
		args = [monthlyPayment, tradeInAllowance, tradeInLoanBalance, downPaymentAndRebates, loanDuration, salesTaxRate, interestRate]
		ret = None
		def CalcAffordability_Ret(async_ret):
			nonlocal ret
			ret = async_ret
		pybus.call('CarLoanCalculator.CalcAffordability', args, CalcAffordability_Ret)
		return ret



