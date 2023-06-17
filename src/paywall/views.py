import logging
from email.mime.application import MIMEApplication
import requests
import os

from django.conf import settings
from django.core import mail
from django.http.response import FileResponse, HttpResponseBadRequest, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.views.generic import FormView
from django.http import HttpResponse, JsonResponse

from seedrs_bot.utils import seedrs
from seedrs_bot.utils import proxy_manager

from . import forms
from seedlense.settings import SEEDRS_USERNAME, SEEDRS_PASSWORD
from seedlense.settings import WEBSHARE_KEY, WEBSHARE_USER, WEBSHARE_PW

logging.basicConfig()
logger = logging.getLogger()
logger.setLevel(logging.INFO)

class Paywall(FormView):
    form_class = forms.PaywallForm
    template_name = 'form.html'
    success_url = '/paywall/my_requests'

    def get(self, request):
        form_class = self.get_form_class()
        form = self.get_form(form_class)

        if form.is_valid():
            page_data = {"title": "Hello Word", "body": "Not much to say."}

            response = HttpResponseRedirect('/')
            response['page_data'] = page_data

            return response

        return self.form_invalid(form)

    def post(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        form = self.get_form(form_class)

        if form.is_valid():
            message = form.data.copy()
            message["username"] = request.user.username

            bypass_resp = requests.get(os.environ['BYPASS_PAYWALL_URL'])
            print(bypass_resp.text)

            return self.form_valid(form)
        return self.form_invalid(form)
