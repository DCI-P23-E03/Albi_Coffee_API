from django.test import TestCase
from rest_framework.test import APIClient,APITestCase
from rest_framework import status
from django.urls import reverse
from django.utils.text import slugify 
from .models import Beer,Brewery
from .serializers import BeerSerializer,BrewerySerializer
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token


class BreweryTests(APITestCase):

    def setUp(self):
        self.client = APIClient()
        self.admin_user = User.objects.create_superuser(
            'admin','admin@test.py','testpassword'
        )
        self.token = Token.objects.create(user=self.admin_user)
        self.user= User.objects.create_user("user", "admin@test.com", "testpassword")
        self.user_token = Token.objects.create(user=self.user)
        self.brewery = Brewery.objects.create(
            name="2 of Us Brewing Company",
            location="Frankfurt"
        )
        self.valid_payload = {
            "name": "1 of Us Brewing Company",
            "location": "Frankfurt"
        }
        self.invalid_payload = {
            "name": "",
            "location": ""
        }

    def test_get_all_breweries(self):
        response = self.client.get(reverse('brewery-list'))
        breweries = Brewery.objects.all()
        serializer = BrewerySerializer(breweries,many=True)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code,status.HTTP_200_OK)

    def test_get_single_brewery(self):
        response = self.client.get(reverse('brewery-detail',args=[self.brewery.id]))
        brewery = Brewery.objects.get(id=self.brewery.id)
        serializer = BrewerySerializer(brewery)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_valid_brewery(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token.key)
        response = self.client.post(
            reverse("brewery-list"), data=self.valid_payload, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_brewery_as_user(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.user_token.key)
        url = reverse("brewery-list")
        data = {
            "name":"New name",
            "location": "New location"
        }
        response = self.client.post(url,data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    def test_authentication_required_for_post_brewery(self):
        url = reverse('brewery-list')
        response = self.client.post(url,data=self.valid_payload,format='json')
        self.assertEqual(response.status_code,status.HTTP_401_UNAUTHORIZED)
    
    def test_create_invalid_brewery(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token.key)
        response = self.client.post(reverse('brewery-list'),data=self.invalid_payload,format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_brewery(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token.key)      
        updated_payload = self.valid_payload.copy()
        updated_payload['name'] = "1 of Us of Brewing Company Revised"
        response = self.client.put(
            reverse('brewery-detail',args=[self.brewery.id]),
            data=updated_payload,
            format='json'
            )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(slugify(response.data['name']),slugify(updated_payload["name"]))
        
    
    
    def test_delete_brewery(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token.key)
        response = self.client.delete(reverse("brewery-detail",args=[self.brewery.id]))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)   



#beer Testing
class BeerTests(APITestCase):

    def setUp(self):

        self.client = APIClient()
        self.admin_user = User.objects.create_superuser(
            'admin','admin@test.py','testpassword'
        )
        self.token = Token.objects.create(user=self.admin_user)
        self.user = User.objects.create_user("user", "admin@test.com", "testpassword")
        self.user_token = Token.objects.create(user = self.user)
        self.brewery = Brewery.objects.create(
            name="Long Lone Star Pilsner",
            location = "rostock"
        )
        self.beer = Beer.objects.create(
            name = "premium pilsners",
            style = "lager",
            abv = 3.5,
            brewery = self.brewery
        )

        self.valid_payload = {
            
            "name":"Lone Star ",
            "style":"ale",
            "abv":4.7,
            "brewery":{
                
                "name":"heidelberg_brewery11",
                "location":"heidelberg"
            }
        }

        self.invalid_payload = {
            "name": "",
            "style": "",
            "abv": "",
            "brewery":{
                "name":"",
                "location":""
            }
        }

    def test_get_all_beers(self):
        response = self.client.get(reverse('beer-list'))
        beers= Beer.objects.all()    
        serializer = BeerSerializer(beers,many=True)
        self.assertEqual(response.data,serializer.data)
        self.assertEqual(response.status_code,status.HTTP_200_OK)
    
    def test_get_single_beer(self):
        response = self.client.get(reverse('beer-detail',args=[self.beer.id]))
        beers = Beer.objects.get(id=self.beer.id)
        serializer = BeerSerializer(beers)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_valid_beer(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token.key)
        response = self.client.post(
            reverse("beer-list"), data=self.valid_payload, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

       
    def test_create_beer_as_user(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.user_token.key)
        url = reverse("beer-list")
        data = {
            
            "name": "New Name",
            "style": "New Style",
            "abv":"3.2",
            "brewery": {
                "name": "New Name",
                "location": "New Location"
            }
        }
        response = self.client.post(url,data,format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_authentication_required_for_post_beer(self):
        url = reverse('beer-list')
        response = self.client.post(url,data=self.valid_payload,format='json')
        self.assertEqual(response.status_code,status.HTTP_401_UNAUTHORIZED)

    def test_create_invalid_beer(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token.key)
        response = self.client.post(reverse('beer-list'),data=self.invalid_payload,format='json')        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_beer(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token.key)      
        updated_payload = self.valid_payload.copy()
        updated_payload['name'] = "Lone Star Revised"
        response = self.client.put(
            reverse('beer-detail',args=[self.beer.id]),
            data=updated_payload,
            format='json'
            )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(slugify(response.data['name']),slugify(updated_payload["name"]))

    def test_delete_beer(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token.key)
        response = self.client.delete(reverse("beer-detail", args=[self.beer.id]))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    
              