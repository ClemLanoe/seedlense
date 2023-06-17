from django.urls import path
from django.contrib.auth.decorators import login_required

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('company/sm_trades', views.CompanyTrades.as_view(), name = 'company_sm_trades'),
    path('buyer_seller/', views.BuyerSeller.as_view(), name = 'buyer_seller'),
]
