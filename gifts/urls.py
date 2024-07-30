from django.urls import path
from .views import GetOrSendGiftsView, RedeemCoinView

urlpatterns = [
    path("getOrSendGift/", GetOrSendGiftsView.as_view(),),
    path("redeemCoins/", RedeemCoinView.as_view())
]
