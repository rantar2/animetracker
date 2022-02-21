from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.views import APIView
from .models import *
from rest_framework.response import Response
from .serializers import *

# Create your views here.
class UserView(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()

class SearchView(APIView):
    serializer_class = SearchSerializer

    def get(self, request):
        detail = [{"userName": detail.userName} for detail in Search.objects.all()]
        return Response(detail)

    def post(self, request):
        serializer = SearchSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)
