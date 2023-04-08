import boto3
import datetime
import os
import tempfile
import threading
import requests
import json
from email.mime.application import MIMEApplication

from django.conf import settings
from django.core import mail
from django.http.response import FileResponse, HttpResponseBadRequest
from django.shortcuts import redirect, render
from django.views.generic import FormView
from django.http import HttpResponse, JsonResponse

from seedrs_bot.utils import seedrs
from seedrs_bot.utils import proxy_manager

from . import forms
from myseedrs.settings import SEEDRS_USERNAME, SEEDRS_PASSWORD, WEBSHARE_KEY

def index(request):
    return render(request, 'tools/index.html')


def portfolio_valuation(request):
    return HttpResponse("Get your current portfolio valuation")

class CompanyTrades(FormView):
    form_class = forms.CompanyTradesForm
    template_name = 'form.html'
    success_url = '/tools/company/sm_trades'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form_title"] = "Get company SM trades"
        # context["takes_files"] = True
        return context

    def post(self, request):
        form_class = self.get_form_class()
        form = self.get_form(form_class)

        if form.is_valid():
            company_id = int(request.POST["company_id"])

            session = requests.Session()
            session.proxies.update(proxy_manager.get_proxy())
            seedrs.log_in(session, SEEDRS_USERNAME, SEEDRS_PASSWORD)

            company_sm_trades = seedrs.get_share_lots(session, company_id, availability='sold')

            return JsonResponse(company_sm_trades, safe=False)

        return self.form_invalid(form)

class BuyerSeller(FormView):
    form_class = forms.BuyersSellersForm
    template_name = 'form.html'
    success_url = '/tools/buyer_seller/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form_title"] = "Get buyers and sellers"
        # context["takes_files"] = True
        return context

    def post(self, request):
        form_class = self.get_form_class()
        form = self.get_form(form_class)

        if form.is_valid():
            tmp_buyer = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf").name
            tmp_seller = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf").name

            print(tmp_buyer, tmp_seller)

            share_lot_id = str(request.POST["share_lot_id"])

            session = requests.Session()
            session.proxies.update(proxy_manager.get_proxy(WEBSHARE_KEY))
            seedrs.log_in(session, SEEDRS_USERNAME, SEEDRS_PASSWORD)

            transaction_data = seedrs.get_transactors(session, share_lot_id, tmp_buyer, tmp_seller)

            return JsonResponse(transaction_data, safe=False)

        return self.form_invalid(form)


def company_sm_trades(request, trades):
    return render(request, "/tools/company/sm_trades/view", context=company_sm_trades)
