from api.viewsets import QuestionsViewSet, TagsViewSet
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'questions', QuestionsViewSet, basename='questions')
router.register(r'tags', TagsViewSet, basename='tags')
