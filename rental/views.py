from django.shortcuts import render, render_to_response
from django.views import generic
from django.http import HttpResponseRedirect, HttpResponse
from django.template import loader, Context
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from graphos.sources.simple import SimpleDataSource
from graphos.renderers.gchart import PieChart, LineChart, AreaChart
from decimal import *

from .more_functions import get_loan_balance
from .models import Analysis
from .forms import InputForm #_description, InputForm_finance, InputForm_income, InputForm_fixed_ex, InputForm_variable_ex, InputForm_future

@login_required(login_url="/property_analyzer/login/")
def input(request):
	if request.method == 'POST':
		form = InputForm(request.POST)
		# form_fin = InputForm_finance(request.POST)
		# form_inc = InputForm_income(request.POST)
		# form_fix_ex = InputForm_fixed_ex(request.POST)
		# form_var_ex = InputForm_variable_ex(request.POST)
		# form_future = InputForm_future(request.POST)
		if form.is_valid():

			# check for 0 values e.g. in amt_years!!
			data=form.cleaned_data
			total_cost=data['price']+data['repair_cost']+data['closing_cost']
			down=int(data['price']*data['down_payment']/100)
			loan_amt=data['price']-down
			R=data['loan_rate']/100/12 # periodic interest rate
			monthly_PI=float((loan_amt*R)/(1-(1+R)**(-12*data['amt_years'])))
			total_cash=data['closing_cost']+down+data['repair_cost']+data['loan_points']/100*loan_amt

			monthly_in=data['rent']+data['other_income']
			monthly_ex=float(data['electric']+data['water_sewer']+data['pmi']+data['garbage']+data['hoa']+data['insurance']+data['taxes']+data['ex_other']) \
					+ float(monthly_in*(data['vacancy']+data['repairs']+data['cap_ex']+data['management'])/100) \
					+ float(monthly_PI)
			monthly_cf=monthly_in-monthly_ex
			NOI=(monthly_in-monthly_ex+monthly_PI)*12
			pro_forma_cap=NOI/data['arv']		
			CoC_roi=monthly_cf*12/total_cash
			purchase_cap=NOI/data['price']
			percent_rule=monthly_in/data['price']*100
			initial_equity=data['arv']-data['price']-data['repair_cost']+down
			GRM=data['price']/(monthly_in*12)
			DCR=NOI/(12*monthly_PI)

			# initialize yearly values with first year and rest 0s
			yearly_in=[monthly_in*12]+[0]*(data['amt_years']-1)
			yearly_ex=[monthly_ex*12]+[0]*(data['amt_years']-1)
			yearly_mg=[monthly_PI*12]*(data['amt_years']) # constant
			yearly_op=[yearly_ex[0]-yearly_mg[0]]+[0]*(data['amt_years']-1)
			yearly_cf=[yearly_in[0]-yearly_ex[0]]+[0]*(data['amt_years']-1)
			yearly_cc=[yearly_cf[0]/total_cash*100]+[0]*(data['amt_years']-1)
			yearly_pv=[data['arv']+data['arv']*data['annual_propvalue_growth']/100]+[0]*(data['amt_years']-1)
			yearly_ba=[get_loan_balance(loan_amt,monthly_PI,data['loan_rate'])]+[0]*(data['amt_years']-1)
			yearly_eq=[yearly_pv[0]-yearly_ba[0]]+[0]*(data['amt_years']-1)
			yearly_pr=[yearly_pv[0]-yearly_ba[0]-total_cash-(data['sales_ex']/100*yearly_pv[0])+yearly_cf[0]]+[0]*(data['amt_years']-1)
			yearly_ar=[yearly_pr[0]/total_cash]+[0]*(data['amt_years']-1)

			# now fill in the rest of the years
			for i in range(1,data['amt_years']):
				yearly_in[i]=yearly_in[i-1]+yearly_in[i-1]*data['annual_income_growth']/100
				yearly_op[i]=yearly_op[i-1]+yearly_op[i-1]*data['annual_ex_growth']/100
				yearly_ex[i]=yearly_op[i]+yearly_mg[i]
				yearly_cf[i]=yearly_in[i]-yearly_ex[i]
				yearly_cc[i]=yearly_cf[i]/total_cash*100
				yearly_pv[i]=yearly_pv[i-1]+yearly_pv[i-1]*data['annual_propvalue_growth']/100
				yearly_ba[i]=get_loan_balance(yearly_ba[i-1],monthly_PI,data['loan_rate'])
				yearly_eq[i]=yearly_pv[i]-yearly_ba[i]
				total_cf=yearly_cf[0]
				for j in range(1,i+1):
					total_cf=total_cf+yearly_cf[j]
				yearly_pr[i]=yearly_pv[i]-yearly_ba[i]-total_cash-(data['sales_ex']/100*yearly_pv[i])+total_cf
				yearly_ar[i]=(1+yearly_pr[i]/total_cash)**(1/i+1)-1

			# designate which years to tabulate
			if(data['amt_years']<11):
				show_years=list(range(0,data['amt_years']))
			elif(data['amt_years']<16):
				show_years=[1,2,5,10]+[data['amt_years']]
			elif(data['amt_years']<21):
				show_years=[1,2,5,10,15]+[data['amt_years']]
			elif(data['amt_years']<26):
				show_years=[1,2,5,10,15,20]+[data['amt_years']]
			elif(data['amt_years']<31):
				show_years=[1,2,5,10,15,20]+[data['amt_years']]		
			else:
				show_years=[1,2,5,10,15,20,30]+[data['amt_years']]		

			vals={
				'title':data['address_st']+', '+data['address_city']+', '+data['address_state']+' '+data['address_zip'],
				'price':data['price'],
				'closing_cost':data['closing_cost'],
				'repair_cost':data['repair_cost'],
				'total_cost':total_cost,
				'arv':data['arv'],
				'down':down,
				'loan_amt':loan_amt,
				'loan_points':data['loan_points']/100*loan_amt,
				'amt_years':data['amt_years'],
				'loan_rate':data['loan_rate'],
				'monthly_PI':monthly_PI,
				'monthly_in':monthly_in,
				'monthly_ex':monthly_ex,
				'monthly_cf':monthly_cf,
				'pro_forma_cap':pro_forma_cap*100,
				'NOI':NOI,
				'total_cash':total_cash,
				'CoC_roi':CoC_roi*100,
				'purchase_cap':purchase_cap*100,
				'yearly_in':yearly_in,
				'yearly_ex':yearly_ex,
				'yearly_mg':yearly_mg,
				'yearly_op':yearly_op,
				'yearly_cf':yearly_cf,
				'yearly_cc':yearly_cc,
				'yearly_pv':yearly_pv,
				'yearly_ba':yearly_ba,
				'yearly_eq':yearly_eq,
				'yearly_pr':yearly_pr,
				'yearly_ar':yearly_ar,
				'show_years':show_years,
				'show_years_index':[x-1 for x in show_years]
			}

			### plotting with graphos ###

			## pie chart
			piechart_list=[['Category','Amount']]
			# fixed expenses
			ex_display_names={'electric':'Electric','water_sewer':'Water &amp; Sewer','pmi':'PMI','garbage':'Garbage','hoa':'HOA','insurance':'Insurance','taxes':'Taxes','ex_other':'Other'}
			for ex in ['electric','water_sewer','pmi','garbage','hoa','insurance','taxes','ex_other']:
				if(data[ex]>0):
					piechart_list.append([ex_display_names[ex],data[ex]])
			# percentage of income expenses
			ex_display_names={'vacancy':'Vacancy','repairs':'Repairs','cap_ex':'CapEx','management':'Management'}
			for ex in ['vacancy','repairs','cap_ex','management']:		
				if(data[ex]>0):
					piechart_list.append([ex_display_names[ex],data[ex]/100*monthly_in])
			if(monthly_PI>0):		
				piechart_list.append(['Mortgage',monthly_PI])		
			piechart = PieChart(SimpleDataSource(data=piechart_list),options={'title':'Expenses'})

			## line chart
			linechart_list=[['Year','Income','Expenses','Cash Flow']]
			for i in range(0,data['amt_years']):
				linechart_list.append([i+1,yearly_in[i],yearly_ex[i],yearly_cf[i]])
			# linechart = LineChart(SimpleDataSource(data=linechart_list),options={'title':'Income, Expenses, and Cash Flow','vAxis':{format:'currency'}})	
			linechart = LineChart(SimpleDataSource(data=linechart_list),options={'title':'Income, Expenses, and Cash Flow'})	

			## area chart
			areachart_list=[['Year','Loan Balance','Equity','Property Value']]
			for i in range(0,data['amt_years']):
				areachart_list.append([i+1,yearly_ba[i],yearly_eq[i],yearly_pr[i]])
			areachart = AreaChart(SimpleDataSource(data=areachart_list),options={'title':'Loan Balance, Value, and Equity'})	

		else:
			print("NAY")
			val=0


		# return render(request, 'selected_data.html',{'fields':fields,'fields_day1':fields_day1,'fields_bat':fields_bat,'fields_img':fields_img,'fields_snp':fields_snp,'subj_data_tuples':subj_data_tuples})
		return render(request, 'output.html',{'vals':vals,'piechart':piechart,'linechart':linechart,'areachart':areachart})
	else:
		form = InputForm()
		# form_fin = InputForm_finance()
		# form_inc = InputForm_income()
		# form_fix_ex = InputForm_fixed_ex()
		# form_var_ex = InputForm_variable_ex()
		# form_future = InputForm_future()

	return render(request, 'input.html',{'form':form})
	# return render(request, 'input.html',{'form_desc':form_desc,'form_fin':form_fin,'form_inc':form_inc,'form_fix_ex':form_fix_ex,'form_var_ex':form_var_ex,'form_future':form_future})