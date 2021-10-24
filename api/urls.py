from django.urls import path
from .views import MentalHealth

urlpatterns = [
    path('response/', MentalHealth.as_view()),
]
