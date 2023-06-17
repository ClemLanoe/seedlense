import boto3
import datetime
import os
import tempfile
import logging
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
from seedlense.settings import SEEDRS_USERNAME, SEEDRS_PASSWORD
from seedlense.settings import WEBSHARE_KEY, WEBSHARE_USER, WEBSHARE_PW

logging.basicConfig()
logger = logging.getLogger()
logger.setLevel(logging.INFO)

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
            company_entry = str(request.POST["company_entry"])
            # entry_type = str(request.POST["entry_type"])

            session = proxy_manager.get_proxied_session(WEBSHARE_KEY, WEBSHARE_USER, WEBSHARE_PW)

            if '.co' in company_entry:
                company_id = seedrs.get_business_id(session, company_entry)
            else:
                company_id = company_entry

            seedrs.log_in(session, SEEDRS_USERNAME, SEEDRS_PASSWORD)

            company_sm_trades = seedrs.get_share_lots(session, company_id, availability='sold', output='filtered')

            session.close()

            return JsonResponse(company_sm_trades, safe=False, json_dumps_params={'indent': 3})

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
        response_type = str(request.POST["response_type"])
        form_class = self.get_form_class()
        form = self.get_form(form_class)

        if form.is_valid():
            tmp_buyer = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf").name
            tmp_seller = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf").name

            share_lot_id = str(request.POST["share_lot_id"])

            session = proxy_manager.get_proxied_session(WEBSHARE_KEY, WEBSHARE_USER, WEBSHARE_PW)
            seedrs.log_in(session, SEEDRS_USERNAME, SEEDRS_PASSWORD)

            transaction_data = seedrs.get_transactors(session, share_lot_id, tmp_buyer, tmp_seller, output=response_type)

            session.close()

            return JsonResponse(transaction_data, safe=False, json_dumps_params={'indent': 3})

        return self.form_invalid(form)

class AllBuyersSellers(FormView):
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

            share_lot_id = str(request.POST["share_lot_id"])

            session = proxy_manager.get_proxied_session(WEBSHARE_KEY, WEBSHARE_USER, WEBSHARE_PW)
            seedrs.log_in(session, SEEDRS_USERNAME, SEEDRS_PASSWORD)

            transaction_data = seedrs.get_transactors(session, share_lot_id, tmp_buyer, tmp_seller)

            session.close()

            return JsonResponse(transaction_data, safe=False, json_dumps_params={'indent': 3})

        return self.form_invalid(form)

def company_sm_trades(request, trades):
    return render(request, "/tools/company/sm_trades/view", context=company_sm_trades)
