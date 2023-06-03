from django import forms
from . import models

# class PaywallForm(forms.ModelForm):
#     def save(self, commit=True):
#         model_instance = super(PaywallForm, self).save(commit=False)

#         model_instance.created_by = self.current_user
#         model_instance.modified_by = self.current_user
#         result = super(PaywallForm, self).save(commit=True)
#         return result
    
#     class Meta:
#         model = models.Paywall

class PaywallForm(forms.Form):
    page_url = forms.CharField(label='Page URL')
