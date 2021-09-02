from django.urls import path

from accounts.views import BalanceAPIView, ResetAPIView
from events.views import EventAPIView

urlpatterns = [
    path('reset', ResetAPIView.as_view(), name='api_reset'),
    path('balance', BalanceAPIView.as_view(), name='api_balance'),
    path('event', EventAPIView.as_view(), name='api_event'),
]
