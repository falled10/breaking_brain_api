from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.permissions import AllowAny

from breaking_brain_api.paginators import ResultSetPagination
from quizzes.models import Quiz
from quizzes.serializers import QuizSerializer


class QuizViewSet(ReadOnlyModelViewSet):
    """
    list:
    Returns list of all quizzes

    Returns list of all quizzes

    retrieve:
    Return one quiz by its id

    Return one quiz by its id
    """

    serializer_class = QuizSerializer
    queryset = Quiz.objects.all()
    permission_classes = (AllowAny,)
    pagination_class = ResultSetPagination
