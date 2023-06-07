from django.db import models
from django_countries.fields import CountryField
from django.utils.functional import cached_property
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
import datetime

from seedrs_bot.utils import general

user_model = get_user_model()

class CurrencyFormats(models.TextChoices):
    GBP = "GBP", _("GBP")
    EUR = "EUR", _("EUR")
    USD = "USD", _("USD")

# Create your models here.
class Business(models.Model):
    seedrs_id = models.IntegerField()
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255, default="")
    url = models.CharField(max_length=255)
    country = CountryField()

    sm_eligibility = models.BooleanField()
    currency = models.CharField(choices=CurrencyFormats.choices, max_length=255)
    valuation = models.DecimalField(max_digits=20, decimal_places=2)
    share_price = models.DecimalField(max_digits=20, decimal_places=2)
    performance = models.DecimalField(max_digits=20, decimal_places=2)
    available_shares = models.DecimalField(max_digits=20, decimal_places=2)
    investors_count = models.IntegerField()
    raising_now = models.BooleanField()

    date_modified = models.DateTimeField(auto_now=True)
    date_added = models.DateTimeField(auto_now_add=True)

    @cached_property
    def last_cycle_volume(self):
        year = general.first_tuesday(last_month=True).year
        month = general.first_tuesday(last_month=True).month
        day = general.first_tuesday(last_month=True).day
        last_cycle_start_date = f"{year}-{month}-{day}"
        last_cycle = Cycles.objects.filter(business=self, cycle_start=last_cycle_start_date).order_by("-date_started")
        if len(last_cycle):
            return last_cycle[0]["trade_volume"]
        else:
            return 0.00

    class Meta:
        db_table = "business"
        verbose_name_plural = "businesses"

class Cycle(models.Model):
    business = models.ForeignKey(Business, on_delete=models.DO_NOTHING)
    cycle_start = models.DateTimeField()
    cycle_end = models.DateTimeField()
    trade_volume = models.IntegerField()

class Person(models.Model):
    name = models.CharField(max_length=255)
    active_on_forums = models.BooleanField()

    class Meta:
        verbose_name_plural = "people"

class Transaction(models.Model):
    buyer = models.ForeignKey(Person, related_name= '+', on_delete=models.DO_NOTHING)
    seller = models.ForeignKey(Person, related_name='+', on_delete=models.DO_NOTHING)
    # Add more fields for transaction #TODO

class ForumPost(models.Model):
    person = models.ForeignKey(Person, on_delete=models.DO_NOTHING)
    post_url = models.CharField(max_length=255)
    post_summary = models.CharField(max_length=255)
