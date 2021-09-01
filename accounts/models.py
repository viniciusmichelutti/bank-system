from django.db import models


class Account(models.Model):
    number = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
