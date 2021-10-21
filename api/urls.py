from django.urls import path
from .views import MentalHealth

urlpatterns = [
    path('responses/', MentalHealth.as_view()), 
]
