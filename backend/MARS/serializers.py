from rest_framework import serializers
from .models import *

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'password')

class SearchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Search
        fields = ['userName']
