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

from myseedrs.settings import SEEDRS_USERNAME, SEEDRS_PASSWORD
from myseedrs.settings import WEBSHARE_KEY, WEBSHARE_USER, WEBSHARE_PW

logging.basicConfig()
logger = logging.getLogger()
logger.setLevel(logging.INFO)

def portfolio(request):
    return render(request, 'portfolio/portfolio.html')