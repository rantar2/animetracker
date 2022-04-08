from rest_framework import serializers
from .models import *

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'password')

class SearchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Search
        fields = ['userName', 'selected_genres']

class AnimeSerializer(serializers.ModelSerializer):
    class Meta:
        model = AnimeEntry
        fields = ['name', 'MAL_ID', 'rank', 'genres', 'main_picture', 'synopsis']
        depth = 1

    def to_representation(self, instance):
        # Override in order to properly display genres
        repr = super().to_representation(instance)
        genreStr = ""
        for genre in repr['genres']:
            genreStr += str(genre["genre_name"]) + ", "
        genreStr = genreStr[:-2]
        repr['genres'] = genreStr
        return repr

class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ["genre_name", "genre_id"]
        depth = 1
