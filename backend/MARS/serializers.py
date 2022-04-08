from rest_framework import serializers
from .models import *

# Used to translate the client's input into readable data for the backend
class SearchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Search
        fields = ['userName', 'selected_genres']

# Used to transform AnimeEntry models from objects in our database into a readable a format, and visa versa
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

# Used to transform Genre models from objects in our database into a readable a format, and visa versa
class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ["genre_name", "genre_id"]
        depth = 1
