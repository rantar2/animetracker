from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.views import APIView
from .models import *
from rest_framework.response import Response
from .serializers import *
from .recommender import Recommender

# Create your views here.
class UserView(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()

class SearchView(APIView):
    serializer_class = SearchSerializer

    def get(self, request):
        print(request)
        return Response("get")

    def post(self, request):
        serializer = SearchSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            #Database.updateDB(1000)  #Adds/replaces first 1000 most popular shows on MAL.
            userList = Recommender.getList(serializer.data["userName"])
            # Below, we limit ourselves to 20 top entries, and 5 genres
            recString = Recommender.recommend(userList, 20, 5)

            return Response(recString)
