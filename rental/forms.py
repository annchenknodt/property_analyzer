from django.contrib.auth.forms import AuthenticationForm 
from django import forms
from django.utils.translation import ugettext_lazy as _, ugettext
from crispy_forms.helper import FormHelper
from crispy_forms import layout, bootstrap
from .models import Analysis

class InputForm(forms.ModelForm):
	class Meta:
		model=Analysis
		fields=['name','address_st','address_city','address_state','address_zip','mls','description',
			'price','arv','closing_cost','repair_cost','down_payment','loan_rate','loan_points','loan_fees','amt_years','typical_cap',
			'rent','other_income',
			'electric','water_sewer','pmi','garbage','hoa','insurance','taxes','ex_other',
			'vacancy','repairs','cap_ex','management',
			'annual_income_growth','annual_propvalue_growth','annual_ex_growth','sales_ex'
			]
		labels={
			"name": "Name for analysis",
			"address_st": "Address street",
			"mls":"MLS #",
			"arv":"After repair value",
			"down_payment":"Down payment (%)",
			"loan_rate":"Loan rate (%)",
			"amt_years":"Amortized over how many years?",
			"typical_cap":"Typical cap rate",
			"water_sewer":"Water/Sewer",
			"pmi":"PMI",
			"hoa":"HOAs",
			"ex_other":"Other",
			"vacancy":"Vacancy (%)",
			"repairs":"Repairs (%)",
			"cap_ex":"Cap Ex (%)",
			"management":"Management (%)",
			"annual_income_growth":"Annual Income Growth (%)",
			"annual_propvalue_growth":"Annual Property Value Growth (%)",
			"annual_ex_growth":"Annual Expenses Growth (%)",
			"sales_ex":"Sales Expenses (%)"

		}

	def __init__(self, *args, **kwargs):
		super(InputForm, self).__init__(*args, **kwargs)

		self.helper = FormHelper()
		self.helper.form_action = ""
		self.helper.form_method = "POST"
		self.helper.field_class = 'col-sm-4'
		self.helper.label_class = 'col-sm-4'		
		self.helper.form_class = 'form-horizontal'

		self.helper.layout = layout.Layout(
		    layout.Fieldset(
		    	_("Basics"),
		    	layout.Field("name"),
		    	layout.Field("address_st", css_class="input-block-level"),
		    	layout.Field("address_city", css_class="input-block-level"),
		    	layout.Field("address_state", css_class="input-block-level"),
		    	layout.Field("address_zip", css_class="input-block-level"),
		    	layout.Field("mls", css_class="input-block-level"),
		    	layout.Field("description", 
					css_class="input-blocklevel", rows="3"),		    ),
		    layout.Fieldset(
		    	_("Financing"),
		    	layout.Field("price", css_class="input-block-level"),
		    	layout.Field("arv", css_class="input-block-level"),
		    	layout.Field("closing_cost", css_class="input-block-level"),
		    	layout.Field("repair_cost", css_class="input-block-level"),
		    	layout.Field("down_payment", css_class="input-block-level"),
		    	layout.Field("loan_rate", css_class="input-block-level"),
		    	layout.Field("loan_points", css_class="input-block-level"),
		    	layout.Field("loan_fees", css_class="input-block-level"),
		    	layout.Field("amt_years", css_class="input-block-level"),
		    	layout.Field("typical_cap", css_class="input-block-level"),
		    ),
		    layout.Fieldset(
		    	_("Income"),
		    	layout.Div(
			    	layout.Div("rent", css_class="col-xs-6"),
			    	layout.Div("other_income", css_class="col-xs-6"),
			    	css_class='row-fluid',
			    )
		    ),		  
		    layout.Fieldset(
		    	_("Fixed Monthly Expenses"),
		    	layout.Div(
			    	layout.Div("electric", css_class="col-xs-3"),
			    	layout.Div("water_sewer", css_class="col-xs-3"),
			    	layout.Div("pmi", css_class="col-xs-3"),
			    	layout.Div("garbage", css_class="col-xs-3"),
			    	css_class='row-fluid',
			    ),
		    	layout.Div(
			    	layout.Div("hoa", css_class="col-xs-3"),
			    	layout.Div("insurance", css_class="col-xs-3"),
			    	layout.Div("taxes", css_class="col-xs-3"),
			    	layout.Div("ex_other", css_class="col-xs-3"),
			    	css_class='row-fluid',
			    )	
			),	
		    layout.Fieldset(
		    	_("Variable Monthly Expenses (as percentage of total income)"),
		    	layout.Div(
			    	layout.Div("vacancy", css_class="col-xs-3"),
			    	layout.Div("repairs", css_class="col-xs-3"),
			    	layout.Div("cap_ex", css_class="col-xs-3"),
			    	layout.Div("management", css_class="col-xs-3"),
			    	css_class='row-fluid',
			    ),
		    
		    ),
			layout.Fieldset(
		    	_("Future Assumptions"),
		    	layout.Div(
			    	layout.Div("annual_income_growth", css_class="col-xs-3"),
			    	layout.Div("annual_propvalue_growth", css_class="col-xs-3"),
			    	layout.Div("annual_ex_growth", css_class="col-xs-3"),
			    	layout.Div("sales_ex", css_class="col-xs-3"),
			    	css_class='row-fluid',
			    )
		    ),
            bootstrap.FormActions(
				layout.Submit('submit', _('Save and calculate')),
            )
        )



		
	# # https://stackoverflow.com/questions/110378/change-the-width-of-form-elements-created-with-modelform-in-django, didn't work when I first tried it
	# def __init__(self, *args, **kwargs):
	# 	super(InputForm, self).__init__(*args, **kwargs) # Call to ModelForm constructor
	# 	self.fields['name'].widget.attrs['cols'] = 10
## maybe try this??
	     # widgets = {
      #       'content': forms.Textarea(attrs={'cols': 80, 'rows': 20})
#       #   }

# class InputForm_finance(forms.ModelForm):
# 	class Meta:
# 		model=Analysis
# 		fields=['price','arv','closing_cost','repair_cost','down_payment','loan_rate','loan_points','loan_fees','amt_years','typical_cap']


# class InputForm_income(forms.ModelForm):
# 	class Meta:
# 		model=Analysis
# 		fields=['rent','other_income']

# class InputForm_fixed_ex(forms.ModelForm):
# 	class Meta:
# 		model=Analysis
# 		fields=['electric','pmi','garbage','hoa','insurance','taxes','ex_other']

# class InputForm_variable_ex(forms.ModelForm):
# 	class Meta:
# 		model=Analysis
# 		fields=['vacancy','repairs','cap_ex','management']

# class InputForm_future(forms.ModelForm):
# 	class Meta:
# 		model=Analysis
# 		fields=['annual_income_growth','annual_propvalue_growth','annual_ex_growth','sales_ex']

