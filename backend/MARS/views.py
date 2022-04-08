from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.views import APIView
from .models import *
from rest_framework.response import Response
from .serializers import *
from .recommender import Recommender
from .MARSdb import Database
from rest_framework.renderers import JSONRenderer
import json

# Create your views here.
class UserView(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()

class SearchView(APIView):
    serializer_class = SearchSerializer

    def get(self, request):
        #print(request)
        returnString = "{\"genre_list\":["
        for item in Genre.objects.all():
            serializer = GenreSerializer(item)
            content = JSONRenderer().render(serializer.data).decode("utf-8")
            #print(content)
            returnString += content + ","
        returnString = returnString[:-1]
        returnString += "]}"
        return Response(returnString)

    def post(self, request):
        serializer = SearchSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            selectedGenres = json.loads(serializer.data["selected_genres"])
            #Database.updateDB(1000)  #Adds/replaces first 1000 most popular shows on MAL.
            userList = Recommender.getList(serializer.data["userName"])
            # Below, we limit ourselves to 20 top entries, and 5 genres
            recString = Recommender.recommend(userList, selectedGenres, 20, 5)

            return Response(recString)
