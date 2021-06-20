from django.urls import path

from recommendation_system.views import RecommendQuizzesView

urlpatterns = [
    path('', RecommendQuizzesView.as_view(), name='recommend-quizzes')
]
