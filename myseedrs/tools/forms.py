from django import forms
from django.core.validators import FileExtensionValidator

class BuyersSellersForm(forms.Form):
    # file = forms.FileField(
    #     label="",
    #     allow_empty_file=False,
    #     validators=[FileExtensionValidator(allowed_extensions=["xlsx"])],
    #     help_text=""
    # )

    # roundtables = forms.IntegerField(widget=forms.Select(choices=[(i, i) for i in range(1, 11)]), initial=1)
    # sessions = forms.IntegerField(widget=forms.Select(choices=[(i, i) for i in range(1, 11)]), initial=1)
    # blanks = forms.IntegerField(widget=forms.Select(choices=[(i, i) for i in range(0, 401, 50)]), initial=250)

    # # Advanced settings
    # seed = forms.IntegerField(widget=forms.Select(choices=[(i, i) for i in range(1, 11)]), initial=3,
    #     help_text="Don't change this value without guidance.")
    # deviation = forms.IntegerField(widget=forms.Select(choices=[(i, i) for i in range(1, 101)]), initial=1,
    #     help_text="Don't change this value without guidance.")
    # iterations = forms.IntegerField(widget=forms.Select(choices=[(i, i) for i in range(1, 10)]), initial=5,
    #     help_text="Don't change this value without guidance.")
    
    company_id = forms.IntegerField()