from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path("buyer_seller/", views.BuyerSeller.as_view(), name = "buyer_seller"),
    path('portfolio_valuation/', views.portfolio_valuation,name='portfolio_valuation')
]
