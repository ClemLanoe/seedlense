from django import forms
from django.core.validators import FileExtensionValidator

ENTRY_TYPES= [
    ('url', 'URL'),
    ('company_id', 'ID'),
    ]

class CompanyTradesForm(forms.Form):
    company_entry = forms.CharField(label="Company URL or ID")
    entry_type = forms.CharField(label='Entry Type', widget=forms.Select(choices=ENTRY_TYPES))

class BuyersSellersForm(forms.Form):
    share_lot_id = forms.CharField()

