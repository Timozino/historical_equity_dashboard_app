from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.views.generic import TemplateView
import MetaTrader5 as mt
import time
from MetaTrader5 import *
from django.utils import timezone
from datetime import timedelta
from .models import TradingAccount, TradingAccountData
from rest_framework import viewsets
from .serializers import TradingAccountSerializer
from django.http import JsonResponse


from django.views import View



class PopulateTradingAccountsView(View):
    '''Objective is to populate the database with these details'''
    
    def get(self, request):
        account_details =  [
            {
                 'server': 'Deriv-Demo',
                 'login': '22014542',
                 'investor_password': 'duzftxd8',
                 'platform': 'MT5'
             },
             {
                 'server': 'ICMarketsEU-Demo',
                 'login': '51135132',
                 'investor_password': 'yym2fmut',
                 'platform': 'MT5'
             },
             {
                 'server': 'ICMarketsEU-Demo',
                 'login': '51135134',
                 'investor_password': 'u5qoleim',
                 'platform': 'MT5'
             }
         ]

        for account in account_details:
            # Create a new TradingAccount instance and set its attributes
            new_account = TradingAccount()
            new_account.server = account['server']
            new_account.login = account['login']
            new_account.investor_password = account['investor_password']
            new_account.platform = account['platform']

            # Save the new TradingAccount instance to the database
            new_account.save()

        return HttpResponse("Trading accounts populated successfully.")




class MT5Trader:
    '''Objective is to initiate log in to the MT5Trader site
    with the login details provided, 
    close connections and re-open after 1 min'''
    
    def __init__(self, login):
        self.trading_account = TradingAccount.objects.get(login=login)
        
    def start_mt5(self):
        # Ensure that all variables are the correct type
        uname = int(self.trading_account.login) # Username must be an int
        pword = str(self.trading_account.investor_password) # Password must be a string
        trading_server = str(self.trading_account.server) # Server must be a string
        filepath = str(self.trading_account.platform) # Filepath must be a string

        # Attempt to start MT5
        if mt.initialize():
            # Login to MT5
            if mt.login(login=uname, password=pword, server=trading_server):
                return True
            else:
                raise PermissionError("Login Fail")
        else:
            raise ConnectionAbortedError("MT5 Initialization Failed")

    def initialize_symbols(self, symbol_array):
        # Start MT5
        if not self.start_mt5():
            raise ConnectionError("Connection Error")

        # Get a list of all symbols supported in MT5
        all_symbols = mt.symbols_get()
        # Create an array to store all the symbols
        symbol_names = []
        # Add the retrieved symbols to the array
        for symbol in all_symbols:
            symbol_names.append(symbol.name)

        # Check each symbol in symbol_array to ensure it exists
        for provided_symbol in symbol_array:
            if provided_symbol in symbol_names:
                # If it exists, enable
                if not mt.symbol_select(provided_symbol, True):
                    raise ValueError("Failed to enable symbol {}".format(provided_symbol))
            else:
                raise SyntaxError("Symbol {} does not exist".format(provided_symbol))

        # Return true when all symbols enabled
        return True

    def get_trading_account_data(self):
        # Initialize symbols for the trading account
        symbol_array = ["EURUSD", "GBPUSD", "USDJPY"]
        self.initialize_symbols(symbol_array)

        # Get the trading account data
        account_data = {}
        account_data['login'] = self.trading_account.login
        account_data['equity'] = mt.AccountInfo().equity
        account_data['balance'] = mt.AccountInfo().balance
        account_data['market_watch_time'] = mt.MarketInfo("EURUSD").time

        # Shutdown the connection to the trading account
        mt.shutdown()

        return account_data

    # def get_account_data_at_interval(self, interval=60):
    #     while True:
    #         account_data = self.get_trading_account_data()
    #         yield account_data
    #         time.sleep(interval)
    def get_account_data_at_interval(self, interval=60):
        while True:
            trading_account_data = {}
            for trading_account in TradingAccount.objects.all():
                # Get the trading account data
                account_data = {}
                account_data['login'] = trading_account.login
                account_data['equity'] = mt.AccountInfo().equity
                account_data['balance'] = mt.AccountInfo().balance
                account_data['market_watch_time'] = mt.MarketInfo("EURUSD").time

                # Add login data to account_data
                account_data.update([trading_account.login])

                trading_account_data[trading_account.id] = account_data

            yield trading_account_data
            time.sleep(interval)
            
class MT5TraderView(View):
    def get(self, request, login):
        trader = MT5Trader(login)
        account_data = trader.get_trading_account_data()
        return JsonResponse(account_data)

class AccountDataView(View):
    '''Objective is to fetch equity and balance data and save it to database every 60 secs'''
    def get(self, request):
        # Define trading account IDs and symbol array
        trading_account_ids = [1, 2, 3]
        symbol_array = ["EURUSD", "GBPUSD", "USDJPY"]

        # Create an MT5Trader instance for each trading account ID
        traders = [MT5Trader(login=account.login, investor_password=account.investor_password, server=account.server, platform=account.platform) for account in TradingAccount.objects.filter(pk__in=trading_account_ids)]

        # Infinite loop to get trading account data at 1-minute interval
        while True:
            for i, trader in enumerate(traders):
                # Get the trading account data using the MT5Trader instance
                account_data = trader.get_trading_account_data()

                # Create a TradingAccountData instance and save it to the database
                trading_account = TradingAccount.objects.get(pk=trading_account_ids[i])
                timestamp = timezone.now()
                equity = account_data['equity']
                balance = account_data['balance']
                TradingAccountData.objects.create(trading_account=trading_account, timestamp=timestamp, equity=equity, balance=balance)

            # Sleep for 1 minute
            time.sleep(60)

            return HttpResponse("Trading account data update started.")





class DashboardView(TemplateView):
    '''Objective is to take the stored data from MT5-Trader and renders it in form of graph in frontend'''
    template_name = 'dashboard/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Retrieve trading account data from the database
        trading_accounts = TradingAccount.objects.all()
        trading_account_data = {}
        for trading_account in trading_accounts:
            trading_account_data[trading_account.id] = TradingAccountData.objects.filter(
                trading_account_id=trading_account.id
            ).order_by('timestamp')

        context['trading_account_data'] = trading_account_data

        return context




class TradingAccountDataView(TemplateView):
    template_name = 'dashboard/trading_account.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        accounts_data = TradingAccountData.objects.all().select_related('trading_account')
        accounts = []
        for data in accounts_data:
            account = data.trading_account
            account.market_watch_time = data.timestamp
            account.equity = data.equity
            account.balance = data.balance
            accounts.append(account)
        context['accounts'] = accounts
        return context



#This view serializes the queryset
class TradingAccountViewSet(viewsets.ModelViewSet):
    queryset = TradingAccount.objects.all()
    serializer_class = TradingAccountSerializer


