from django.db import models
from datetime import datetime, timedelta
import pytz
from MetaTrader5 import *

class TradingAccount(models.Model):
    login = models.PositiveIntegerField()
    investor_password = models.CharField(max_length=50)
    server = models.CharField(max_length=50)
    platform = models.CharField(max_length=200)
    slug=models.SlugField()

    def __str__(self):
        return f'{self.server} - {self.login}'

class TradingAccountData(models.Model):
    trading_account = models.ForeignKey(TradingAccount, on_delete=models.CASCADE)
    timestamp = models.DateTimeField()
    equity = models.FloatField()
    balance = models.FloatField()

    class Meta:
        ordering = ['timestamp']

    def __str__(self):
        return f"{self.trading_account.server} - {self.trading_account.login} - {self.timestamp}"
