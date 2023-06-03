from django.urls import path

from . import views

urlpatterns = [
    path('', views.Paywall.as_view(), name = 'paywall'),
]
