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

class AnimeSerializer(serializers.ModelSerializer):
    class Meta:
        model = AnimeEntry
        fields = ['name', 'animeID', 'rank', 'genres', 'main_picture', 'synopsis']