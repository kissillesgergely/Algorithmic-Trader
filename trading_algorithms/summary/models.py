from django.db import models
from django.utils import timezone

class Trade(models.Model):
    stock = models.CharField(default=None, max_length=10)
    #The following field must be sell or buy
    side = models.CharField(default=None, max_length=4)
    date_of_open = models.DateTimeField(default=timezone.now)
    date_of_close = models.DateTimeField(default=None, blank=True, null=True)
    open_price = models.FloatField(default=None)
    close_price = models.FloatField(default=None, blank=True, null=True)

    def __str__(self):
        return str(self.date_of_open) + ' ' + self.stock + ' ' + str(self.open_price)
