from api.viewsets import *
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'questions', QuestionsViewSet, basename='questions')
router.register(r'tags', TagsViewSet, basename='tags')
router.register(r'posts', PostsViewSet, basename='posts')
router.register(r'users', UsersViewSet, basename='users')
router.register(r'responses', ResponsesViewSet, basename='responses')
