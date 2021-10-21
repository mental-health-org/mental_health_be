from api.viewsets import QuestionsViewSet, TagsViewSet, PostsViewSet
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'questions', QuestionsViewSet, basename='questions')
router.register(r'tags', TagsViewSet, basename='tags')
router.register(r'posts', PostsViewSet, basename='posts')
