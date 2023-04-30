from django import forms
from django.core.validators import FileExtensionValidator

ENTRY_TYPES= [
    ('url', 'URL'),
    ('company_id', 'ID'),
    ]

RESPONSE_TYPES = [
    ('simple', 'Simple'),
    ('full', 'Full'),
]

class CompanyTradesForm(forms.Form):
    company_entry = forms.CharField(label="Company URL or ID")
    # entry_type = forms.CharField(label='Entry Type', widget=forms.Select(choices=ENTRY_TYPES))

class BuyersSellersForm(forms.Form):
    share_lot_id = forms.CharField()
    response_type = forms.CharField(label='Response Type', widget=forms.Select(choices=RESPONSE_TYPES))

