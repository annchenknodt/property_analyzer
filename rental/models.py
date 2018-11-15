from django.db import models
from decimal import Decimal

class Analysis(models.Model):
	created_at = models.DateTimeField(auto_now_add=True)
	# description
	name=models.CharField(max_length=100)	
	address_st=models.CharField(max_length=50,default='')
	address_city=models.CharField(max_length=50,default='')
	address_state=models.CharField(max_length=20,default='')
	address_zip=models.CharField(max_length=10,default='')
	mls=models.CharField(max_length=25,default='')
	description=models.TextField(default='')
	# finance
	price=models.IntegerField(default=0)
	arv=models.IntegerField(default=0)
	closing_cost=models.IntegerField(default=0)
	repair_cost=models.IntegerField(default=0)
	down_payment=models.IntegerField(default=20)
	loan_rate=models.DecimalField(decimal_places=3,max_digits=5,default=5.000)
	loan_points=models.IntegerField(default=0)
	loan_fees=models.IntegerField(default=0)
	amt_years=models.IntegerField(default=30)
	typical_cap=models.DecimalField(decimal_places=3,max_digits=5,default=5.000)
	# monthly income
	rent=models.IntegerField(default=0)
	other_income=models.IntegerField(default=0)
	# fixed monthly expenses
	electric=models.IntegerField(default=0)
	water_sewer=models.IntegerField(default=0)
	pmi=models.IntegerField(default=0)
	garbage=models.IntegerField(default=0)
	hoa=models.IntegerField(default=0)
	insurance=models.IntegerField(default=0)
	taxes=models.IntegerField(default=0)
	ex_other=models.IntegerField(default=0)
	# variable monthly expenses (based on % of rent+other income)
	vacancy=models.IntegerField(default=5)
	repairs=models.IntegerField(default=8)
	cap_ex=models.IntegerField(default=8)
	management=models.IntegerField(default=8)
	# future assumptions
	annual_income_growth=models.IntegerField(default=2)
	annual_propvalue_growth=models.IntegerField(default=2)
	annual_ex_growth=models.IntegerField(default=2)
	sales_ex=models.IntegerField(default=10)

	def __str__(self):
		return str(self.id)+"_"+self.name 	

