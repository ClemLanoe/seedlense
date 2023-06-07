from django.contrib import admin
from .models import Business, Cycle, Person, Transaction, ForumPost

admin.site.register([Business, Cycle, Person, Transaction, ForumPost])
