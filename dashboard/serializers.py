from rest_framework import serializers
from .models import TradingAccount

class TradingAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = TradingAccount
        fields = ['id', 'server', 'login', 'platform','investor_password']
       # fields= "__all__"
