from django.test import TestCase, Client
from .models import TradingAccount, TradingAccountData
from django.urls import reverse
from django.contrib.auth.models import User
from unittest.mock import patch
from .views import MT5TraderView
import unittest
from unittest.mock import patch, Mock
from .models import TradingAccount
import MetaTrader5 as MT5Trader


class TestTradingAccountModel(TestCase):
    def setUp(self):
        self.trading_account = TradingAccount.objects.create(
            login=123456,
            investor_password='abc123',
            server='MyServer',
            platform='MT5',
            slug='my-trading-account'
        )

    def test_trading_account_str_method(self):
        expected_output = 'MyServer - 123456'
        self.assertEqual(str(self.trading_account), expected_output)


class TestTradingAccountDataModel(TestCase):
    def setUp(self):
        self.trading_account = TradingAccount.objects.create(
            login=123456,
            investor_password='abc123',
            server='MyServer',
            platform='MT5',
            slug='my-trading-account'
        )
        self.trading_account_data = TradingAccountData.objects.create(
            trading_account=self.trading_account,
            timestamp='2022-01-01 00:00:00',
            equity=1000.00,
            balance=1500.00,
        )

    def test_trading_account_data_str_method(self):
        expected_output = f"{self.trading_account} - {self.trading_account_data.timestamp}"
        self.assertEqual(str(self.trading_account_data), expected_output)











class TestMT5Trader(unittest.TestCase):
    def setUp(self):
        self.trading_account = TradingAccount.objects.create(login=12345, investor_password='test', server='test-server', platform='test-platform')
        self.mt5_trader = MT5Trader(self.trading_account.login)

    def test_initialize_symbols(self):
        with patch('mt5_trader.mt') as mock_mt:
            mock_symbols_get = Mock()
            mock_symbols_get.return_value = [
                Mock(name='EURUSD'),
                Mock(name='GBPUSD'),
                Mock(name='USDJPY')
            ]
            mock_mt.symbols_get = mock_symbols_get
            mock_symbol_select = Mock(return_value=True)
            mock_mt.symbol_select = mock_symbol_select

            self.assertTrue(self.mt5_trader.initialize_symbols(['EURUSD', 'USDJPY']))
            mock_symbols_get.assert_called_once()
            mock_symbol_select.assert_any_call('EURUSD', True)
            mock_symbol_select.assert_any_call('USDJPY', True)

            with self.assertRaises(ValueError):
                mock_symbol_select.return_value = False
                self.mt5_trader.initialize_symbols(['EURUSD'])
            with self.assertRaises(SyntaxError):
                self.mt5_trader.initialize_symbols(['EURUSD', 'USDJPY', 'EURGBP'])

    def test_get_trading_account_data(self):
        with patch('mt5_trader.mt') as mock_mt:
            mock_symbols_get = Mock()
            mock_symbols_get.return_value = [
                Mock(name='EURUSD'),
                Mock(name='GBPUSD'),
                Mock(name='USDJPY')
            ]
            mock_mt.symbols_get = mock_symbols_get
            mock_mt.AccountInfo = Mock(equity=1000, balance=2000)
            mock_market_info = Mock(time=1234567890)
            mock_mt.MarketInfo = Mock(return_value=mock_market_info)

            account_data = self.mt5_trader.get_trading_account_data()
            self.assertEqual(account_data['Login'], self.trading_account.login)
            self.assertEqual(account_data['equity'], 1000)
            self.assertEqual(account_data['balance'], 2000)
            self.assertEqual(account_data['market_watch_time'], 1234567890)
            mock_symbols_get.assert_called_once()
            mock_mt.AccountInfo.assert_called_once()
            mock_mt.MarketInfo.assert_called_once_with('EURUSD')
            mock_mt.shutdown.assert_called_once()
