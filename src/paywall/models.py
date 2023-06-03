from django.db import models
# from django.contrib.auth import get_user_model

# user_model = get_user_model()

# Create your models here.

# class Article(models.Model):
#     user_id = models.ForeignKey(user_model, related_name='+', null=True, on_delete=models.SET_NULL, db_column="user_id")
    
#     title = models.TextField(blank=True, db_column="title")
#     summary = models.TextField(blank=True, db_column="summary")
#     content = models.TextField(blank=True, db_column="content")
#     author = models.CharField(max_length=100, blank=True, db_column="author")
#     url = models.CharField(max_length=255, blank=True, verbose_name="URL", db_column="url")

#     publish_date = models.DateField(db_column="publish_date")
#     publish = models.BooleanField(default=0, db_column="publish")

#     source = models.CharField(max_length=255, blank=True, db_column="source")

#     date_modified = models.DateTimeField(auto_now=True)
#     date_added = models.DateTimeField(auto_now_add=True)

#     class Meta:
#         db_table = "article"

class Paywall(models.Model):
    page_url = models.CharField(db_column="page_url", verbose_name='Page URL', max_length=255)
