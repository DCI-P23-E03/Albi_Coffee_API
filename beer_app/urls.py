# urls.py
from django.urls import path
from .views import BreweryListAPIView, BreweryDetailAPIView, BeerListAPIView, BeerDetailAPIView
from drf_yasg.views import get_schema_view
from drf_yasg import openapi


schema_view = get_schema_view(
    openapi.Info(
        title='Beer API',
        default_version='v1',
        description='API for beers',
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@beerapi.local"),
        license=openapi.License(name="MIT License"),
    ),
    public=True,
    permission_classes=[],
    authentication_classes=[]
    )



urlpatterns = [
    path('breweries/', BreweryListAPIView.as_view(), name='brewery-list'),
    path('breweries/<int:pk>/', BreweryDetailAPIView.as_view(), name='brewery-detail'),
    path('beers/', BeerListAPIView.as_view(), name='beer-list'),
    path('beers/<int:pk>/', BeerDetailAPIView.as_view(), name='beer-detail'),
    path('openapi/', schema_view.without_ui(cache_timeout=0)),
    path('swagger/',schema_view.with_ui('swagger',cache_timeout=0),name='schema-swagger-ui'),
    path('redoc/',schema_view.with_ui('redoc',cache_timeout=0), name='schema-redoc')

]







