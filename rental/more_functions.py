

# Get loan balance after a year
def get_loan_balance(starting_balance,monthly_PI,interest_rate):
	cur_balance=starting_balance
	for i in range(0,12):
		paid_interest=cur_balance*float(interest_rate/100/12)
		paid_principle=monthly_PI-paid_interest
		cur_balance=cur_balance-paid_principle
		print(str(paid_interest)+" "+str(paid_principle)+" "+str(cur_balance))
	return cur_balance