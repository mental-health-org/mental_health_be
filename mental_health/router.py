from api.viewsets import QuestionsViewSet
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'questions', QuestionsViewSet, basename='questions')
