# serializers.py
from typing import Any
from rest_framework import serializers
from .models import Brewery, Beer
from rest_framework.exceptions import ValidationError
from django.utils.html import escape,strip_tags
from django.utils.text import slugify


class UniqueABVNotBeNegativeValidator:
    def __call__(self,value):
        if value < 0:
             
             raise ValidationError("The abv cannot be negative.")

class UniqueBreweryValidator:
    def __call__(self,value):
        if Brewery.objects.filter(name=value).exists():
            raise ValidationError("The brewery already exists.")         

class LocationExistValidator:
    def __call__(self, value):
        if value.lower() not in ['frankfurt','stuttgart','rostock','heidelberg','augsburg']:
            raise ValidationError("Location is not in our system")

class CapitalizeName:
    def __call__(self, value):
        return value.title()


class BrewerySerializer(serializers.ModelSerializer):
    name=serializers.CharField(max_length=200, required=True,validators=[UniqueBreweryValidator(),],trim_whitespace=True)
    location=serializers.CharField(max_length=200,required=True,validators=[LocationExistValidator()])
    def validate_name(self,value):
        return strip_tags(slugify(value))
    
    
    
    class Meta:
        model = Brewery
        #fields = '__all__'
        fields = ['id', 'name', 'location']

#validation
class BeerSerializer(serializers.ModelSerializer):
    brewery = BrewerySerializer()
    #brewery=serializers.CharField(max_length= 200, required=True, validators=[UniqueBreweryValidator()],trim_whitespace=True)
    abv= serializers.FloatField(validators=[UniqueABVNotBeNegativeValidator()])


    def validate_name(self,value):
        return CapitalizeName()(value)
    
    def validate_style(self,value):
        return strip_tags(value)
    
    
    

    class Meta:
        model = Beer
        #fields = '__all__'
        fields = ['id', 'name', 'style', 'abv', 'brewery']
    
    def create(self, validated_data):
        
        brewery_data = validated_data.pop('brewery') #pop
        brewery_instance = Brewery.objects.create(**brewery_data)
        beer_instance = Beer.objects.create(brewery=brewery_instance, **validated_data)
        return beer_instance
    
    
    
    def update(self, instance, validated_data):
        brewery_data = validated_data.pop('brewery', None)

        
        instance.name = validated_data.get('name', instance.name)
        instance.style = validated_data.get('style', instance.style)
        instance.abv = validated_data.get('abv', instance.abv)
        instance.save()

        
        if brewery_data:
            brewery = instance.brewery
            brewery.name = brewery_data.get('name', brewery.name)
            brewery.location = brewery_data.get('location', brewery.location)
            brewery.save()

        return instance






