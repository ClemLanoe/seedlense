import boto3
import datetime
import os
import tempfile
import threading

import pandas as pd

from email.mime.application import MIMEApplication
from io import StringIO

from django.conf import settings
from django.core import mail
from django.http.response import FileResponse, HttpResponseBadRequest
from django.shortcuts import redirect, render
from django.views.generic import FormView
from django.http import HttpResponse

from gfm_utils.file import clean
from gfm_utils.helpers import badges
from gfm_utils.text import preprocessing
from gfm_utils.text import similarity

from . import forms

def index(request):
    return render(request, 'tools/index.html')

def portfolio_valuation(request):
    return HttpResponse("Get your current portfolio valuation")

class BuyerSeller(FormView):
    form_class = forms.BuyersSellersForm
    template_name= 'form.html'
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
            try:
                file = request.FILES.getlist("file")[0]
                tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".xlsx")

                dfs = pd.read_excel(file, sheet_name=None, dtype=str)
                dfs = clean.clean_dfs(dfs)

                # roundtables = int(request.POST["roundtables"])
                # sessions = int(request.POST["sessions"])
                # blanks = int(request.POST["blanks"])
                # seed = int(request.POST["seed"])
                # deviation = int(request.POST["deviation"])
                # iterations = int(request.POST["iterations"])
                iterations = int(request.POST["company_id"])

                badges.badge_creation(dfs, roundtables, sessions, blanks,
                    seed, deviation, iterations, tmp.name)
                
                return FileResponse(
                    open(tmp.name, 'rb'),
                    filename=file.name.replace(".xlsx", "_Output.xlsx")
                )
            finally:
                os.remove(tmp.name)
        return self.form_invalid(form)