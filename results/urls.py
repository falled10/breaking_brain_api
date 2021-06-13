from rest_framework.routers import SimpleRouter
from django.urls import path

from results.views import QuizResultViewSet, CreateQuestionResultView


router = SimpleRouter()
router.register('quizzes', QuizResultViewSet, basename='quizzes-result')

urlpatterns = [
    path('questions/', CreateQuestionResultView.as_view(), name='create-question-result')
] + router.urls
