from django.urls import path, include
from .views import DashboardView
from rest_framework import routers
from .views import TradingAccountViewSet
from .views import PopulateTradingAccountsView
from .views import AccountDataView
from .views import TradingAccountDataView
from .views import MT5TraderView


router = routers.DefaultRouter()
router.register(r'trading-accounts', TradingAccountViewSet)

app_name = 'dashboard'



urlpatterns = [
    path('populate/', PopulateTradingAccountsView.as_view(), name='populate_trading_accounts'),
    #path('trading-account/', TradingAccountView.as_view(), name='trading_account'),
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
    path('mt5-trader/<int:login>/', MT5TraderView.as_view(), name='mt5-trader'),
    path('update_trading_data/', AccountDataView.as_view(), name='update_trading_data'),
    path('trading-account-data/', TradingAccountDataView.as_view(), name='trading_account_data'),
    
    path('', include(router.urls)),
]



