from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from django.utils.functional import cached_property

from secondary_market import models as secondary_market_models

user_model = get_user_model()

class Platforms(models.TextChoices):
    SEEDRS = "Seedrs", _("Seedrs"),
    CROWDCUBE = "Crowdcube", _("Crowdcube"),

class InvestmentRoundType(models.TextChoices):
    PRE_SEED = "Pre-Seed", _("Pre-Seed"),
    SEED = "Seed", _("Seed"),
    SERIES_A = "Series A", _("Series A"),
    CLN = "CLN", _("CLN"),
    SECONDARY = "Secondary", _("Secondary")

class Round(models.Model):
    round_type = models.CharField(choices=InvestmentRoundType.choices, max_length=255)
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

class Article(models.Model):
    business = models.ForeignKey(secondary_market_models.Business, on_delete=models.DO_NOTHING)
    title = models.TextField(blank=True, db_column="title")
    date_published = models.DateField(db_column="date_published")
    summary = models.TextField(blank=True, db_column="summary")
    content = models.TextField(blank=True, db_column="content")
    author = models.CharField(max_length=100, blank=True, db_column="author")
    url = models.CharField(max_length=255, blank=True, verbose_name="URL", db_column="url")
    source = models.CharField(max_length=255, blank=True, db_column="source")
    tags = models.CharField(max_length=255, blank=True, db_column="tags")

    date_modified = models.DateTimeField(auto_now=True)
    date_added = models.DateTimeField(auto_now_add=True)

class BusinessAnalytics(models.Model):
    business = models.ForeignKey(secondary_market_models.Business, on_delete=models.DO_NOTHING)
    website_performance = models.JSONField()
    website_geography = models.JSONField()
    android_app_performance = models.JSONField()
    ios_app_performance = models.JSONField()

    # Add last 3/6/12 months articles
    @cached_property
    def article_count(self):
        business_articles = Article.objects.filter(business=self.business).order_by("-date_published")
        return len(business_articles)

