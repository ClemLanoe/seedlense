from django.db import models
from django_countries.fields import CountryField
from django.utils.functional import cached_property
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

from portfolio import models as portoflio_models

from seedrs_bot.utils import general

user_model = get_user_model()

class CurrencyFormats(models.TextChoices):
    GBP = "GBP", _("GBP")
    EUR = "EUR", _("EUR")
    USD = "USD", _("USD")

class ShareLotStatusTypes(models.TextChoices):
    AVAILABLE = "Available", _("Available")
    SOLD = "Sold", _("Sold")

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
        last_cycle = Cycle.objects.filter(business=self, cycle_start=last_cycle_start_date).order_by("-date_started")
        if len(last_cycle):
            return last_cycle[0]["trade_volume"]
        else:
            return 0.00

    @cached_property
    def business_articles(self):
        business_articles = portoflio_models.Article.objects.filter(business=self).order_by("-date_published")
        return business_articles

    class Meta:
        db_table = "business"
        verbose_name_plural = "businesses"

class Cycle(models.Model):
    business = models.ForeignKey(Business, on_delete=models.DO_NOTHING)
    cycle_start = models.DateTimeField()
    cycle_end = models.DateTimeField()
    trade_volume = models.IntegerField()

    date_modified = models.DateTimeField(auto_now=True)
    date_added = models.DateTimeField(auto_now_add=True)

class Person(models.Model):
    name = models.CharField(max_length=255)
    active_on_forums = models.BooleanField()

    date_modified = models.DateTimeField(auto_now=True)
    date_added = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "people"

class ShareLot(models.Model):
    share_lot_uuid = models.UUIDField()
    business = models.ForeignKey(Business, on_delete=models.DO_NOTHING)
    status = models.CharField(choices=ShareLotStatusTypes.choices, max_length=255)

    share_lot_size = models.DecimalField(max_digits=20, decimal_places=2)
    share_count = models.IntegerField(max_length=255),
    listed_share_price = models.DecimalField(max_digits=20, decimal_places=2)
    original_share_price = models.DecimalField(max_digits=20, decimal_places=2)
    percentage_change = models.DecimalField(max_digits=20, decimal_places=2),
    target_date = models.DateTimeField()

    date_modified = models.DateTimeField(auto_now=True)
    date_added = models.DateTimeField(auto_now_add=True)

    @cached_property
    def share_lot_transaction(self):
        transaction = Transaction.objects.filter(share_lot=self)
        return transaction

class Transaction(models.Model):
    share_lot = models.ForeignKey(ShareLot, on_delete=models.DO_NOTHING)
    buyer = models.ForeignKey(Person, related_name='+', on_delete=models.DO_NOTHING)
    seller = models.ForeignKey(Person, related_name='+', on_delete=models.DO_NOTHING)

    date_modified = models.DateTimeField(auto_now=True)
    date_added = models.DateTimeField(auto_now_add=True)

class ForumPost(models.Model):
    person = models.ForeignKey(Person, on_delete=models.DO_NOTHING)
    business = models.ForeignKey(Business, on_delete=models.DO_NOTHING)
    post_url = models.CharField(max_length=255)
    post_summary = models.CharField(max_length=255)

    date_modified = models.DateTimeField(auto_now=True)
    date_added = models.DateTimeField(auto_now_add=True)

class Alert(models.Model):
    user = models.ForeignKey(user_model, on_delete=models.DO_NOTHING)
    business = models.ForeignKey(Business, on_delete=models.DO_NOTHING)
    max_total_price = models.DecimalField(max_digits=20, decimal_places=2)
    alert_share_price = models.DecimalField(max_digits=20, decimal_places=2)
    persist = models.BooleanField()
    share_lot = models.ForeignKey(ShareLot, on_delete=models.DO_NOTHING)
    last_notification_datetime = models.DateTimeField()

    date_modified = models.DateTimeField(auto_now=True)
    date_added = models.DateTimeField(auto_now_add=True)
