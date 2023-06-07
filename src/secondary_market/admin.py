from django.contrib import admin
from .models import Business, Cycle

admin.site.register([Business, Cycle])
