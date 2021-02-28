from rest_framework.routers import SimpleRouter

from quizzes.views import QuizViewSet


router = SimpleRouter()
router.register('', QuizViewSet, basename='quizzes')


urlpatterns = [

] + router.urls
