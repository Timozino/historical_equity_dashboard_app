from django.contrib import admin
from .models import TradingAccount, TradingAccountData


@admin.register(TradingAccount)
class TradingAccount(admin.ModelAdmin):
    list_display=['server', 'login', 'platform', 'slug']
    list_filter=['platform','server','login']
    search_fields=['server', 'login', 'platform']
   
    prepopulated_fields={'slug':('server','login')}
    
@admin.register(TradingAccountData)
class TradingAccountData(admin.ModelAdmin):
    list_display=['trading_account', 'equity', 'balance']
    list_filter=['trading_account','equity','balance']
    search_fields=['timestamp', 'balance']
    
    
   
