from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('company/sm_trades', views.CompanyTrades.as_view(), name = 'company_sm_trades'),
    path('buyer_seller/', views.BuyerSeller.as_view(), name = 'buyer_seller'),
    path('portfolio_valuation/', views.portfolio_valuation, name='portfolio_valuation')
]
