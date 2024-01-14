from django.shortcuts import render
from rest_framework import generics,permissions
from .models import Brewery, Beer
from .serializers import BrewerySerializer, BeerSerializer
import requests
from .permissions import IsAdminOrReadOnly
from rest_framework.authentication import TokenAuthentication
from drf_yasg.utils import swagger_auto_schema

class BreweryListAPIView(generics.ListCreateAPIView):
    queryset = Brewery.objects.all()
    serializer_class = BrewerySerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAdminOrReadOnly,permissions.IsAuthenticatedOrReadOnly]

    @swagger_auto_schema(operation_description='Retrieve the list of breweries')
    def get(self,request, *args, **kwargs):
        return super().get(request, *args,**kwargs)
    
    @swagger_auto_schema(operation_description='Create a new brewery')
    def post(self,request,*args,**kwargs):
        return super().post(request,*args,**kwargs)

class BreweryDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Brewery.objects.all()
    serializer_class = BrewerySerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAdminOrReadOnly,permissions.IsAuthenticatedOrReadOnly]

    @swagger_auto_schema(operation_description='Retrieve a brewery a id')
    def get(self,request, *args, **kwargs):
        return super().get(request, *args,**kwargs)
    
    @swagger_auto_schema(operation_description='Update a single brewery')
    def put(self,request, *args, **kwargs):
        return super().put(request, *args,**kwargs)


    @swagger_auto_schema(operation_description='Delete a brewery')
    def delete(self,request, *args, **kwargs):
        return super().delete(request, *args,**kwargs)

class BeerListAPIView(generics.ListCreateAPIView):
    #queryset = Beer.objects.all()
    serializer_class = BeerSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAdminOrReadOnly,permissions.IsAuthenticatedOrReadOnly]

    @swagger_auto_schema(operation_description='Retrieve the list of beers')
    def get(self,request, *args, **kwargs):
        return super().get(request, *args,**kwargs)
    
    @swagger_auto_schema(operation_description='Create a new beer')
    def post(self,request,*args,**kwargs):
        return super().post(request,*args,**kwargs)


    def get_queryset(self):
        # Fetch breweries from an external API (Open Brewery DB API)
        external_api_url = 'https://api.openbrewerydb.org/breweries'
        response = requests.get(external_api_url)
        breweries_data = response.json()

        # Create or update breweries in the local database
        for brewery_data in breweries_data:
            brewery, created = Brewery.objects.get_or_create(
                name=brewery_data['name'],
                defaults={'location': brewery_data.get('city', '')}
            )

        # Return the queryset of beers
        return Beer.objects.all()

class BeerDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Beer.objects.all()
    serializer_class = BeerSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAdminOrReadOnly,permissions.IsAuthenticatedOrReadOnly]

    @swagger_auto_schema(operation_description='Retrieve a beer by id')
    def get(self,request, *args, **kwargs):
        return super().get(request, *args,**kwargs)
    
    @swagger_auto_schema(operation_description='Update a single beer')
    def put(self,request, *args, **kwargs):
        return super().put(request, *args,**kwargs)


    @swagger_auto_schema(operation_description='Delete a beer')
    def delete(self,request, *args, **kwargs):
        return super().delete(request, *args,**kwargs)




