from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

from secondary_market import models as secondary_market_models

user_model = get_user_model()

class Platforms(models.TextChoices):
    SEEDRS = "Seedrs", _("Seedrs"),
    CROWDCUBE = "Crowdcube", _("Crowdcube"),

class InvestmentRoundType(models.TextChoices):
    PRE_SEED = "Pre-Seed", _("Pre-Seed"),
    SEED = "Seed", _("Pre-Seed"),
    SERIES_A = "Series A", _("Series A"),
    CLN = "CLN", _("CLN")

class Round(models.Model):
    url = models.CharField(max_length=255)
    business = models.ForeignKey(secondary_market_models.Business, on_delete=models.DO_NOTHING)
    platform = models.CharField(choices=Platforms.choices, max_length=255)
    target = models.DecimalField(max_digits=20, decimal_places=2)
    premoney_valuation = models.DecimalField(max_digits=20, decimal_places=2)
    share_price = models.DecimalField(max_digits=20, decimal_places=2)
    currency = models.CharField(choices=secondary_market_models.CurrencyFormats.choices, max_length=255)

class Investment(models.Model):
    user = models.ForeignKey(user_model, on_delete=models.DO_NOTHING)
    round = models.ForeignKey(Round, on_delete=models.CASCADE)
    invested = models.DecimalField(max_digits=20, decimal_places=2)





    

