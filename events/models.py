from django.db import models

from accounts.models import Account


class Event(models.Model):
    type = models.CharField(max_length=255)
    origin = models.ForeignKey(Account, on_delete=models.DO_NOTHING, null=True, related_name='events_origin')
    destination = models.ForeignKey(Account, on_delete=models.DO_NOTHING, null=True, related_name='events_destination')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
