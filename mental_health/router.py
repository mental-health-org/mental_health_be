from tags.viewsets import *
from account.viewsets import *
from questions.viewsets import *
from responses.viewsets import *
from rest_framework import routers

router = routers.DefaultRouter()

router.register(r'questions', QuestionsViewSet, basename='questions')
router.register(r'qvote', QuestionVoteViewSet, basename='qvote')
router.register(r'qflag', QuestionFlagViewSet, basename='qflag')

router.register(r'responses', ResponsesViewSet, basename='responses')
router.register(r'rvote', ResponseVoteViewSet, basename='rvote')
router.register(r'rflag', ResponseFlagViewSet, basename='rflag')

router.register(r'tags', TagsViewSet, basename='tags')

router.register(r'register', RegisterViewSet, basename='register')
router.register(r'users', UsersViewSet, basename='users')
router.register(r'login', LoginViewSet, basename='login')
router.register(r'logout', LogoutViewSet, basename='logout')

router.register(r'connections', ConnectionViewSet, basename='connections')
