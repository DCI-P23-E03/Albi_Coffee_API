from django.db import models

class Brewery(models.Model):
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=100)

class Beer(models.Model):
    name = models.CharField(max_length=100)
    style = models.CharField(max_length=50)
    abv = models.FloatField() #Acronym: Alcohol by volume
    brewery = models.ForeignKey(Brewery, on_delete=models.CASCADE)

