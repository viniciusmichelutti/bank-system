from django.urls import path

from accounts.views import BalanceAPIView
from events.views import EventAPIView

urlpatterns = [
    path('balance/', BalanceAPIView.as_view(), name='api_balance'),
    path('event/', EventAPIView.as_view(), name='api_event'),
]
