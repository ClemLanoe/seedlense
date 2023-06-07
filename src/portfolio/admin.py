from django.contrib import admin
from .models import Round, Investment

admin.site.register([Round, Investment])
