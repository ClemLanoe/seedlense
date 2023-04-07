from django import forms
from django.core.validators import FileExtensionValidator

class CompanyTradesForm(forms.Form):
    company_id = forms.IntegerField()

class BuyersSellersForm(forms.Form):
    share_lot_id = forms.CharField()
