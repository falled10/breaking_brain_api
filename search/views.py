from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from quizzes.serializers import LessonSerializer, QuizSerializer
from search.utils import search_lessons, search_quizzes


class SearchView(APIView):
    permission_classes = (AllowAny,)

    def get(self, request, *args, **kwargs):
        q = request.GET.get('q', '')
        data = {
            'lessons': LessonSerializer(search_lessons(q).to_queryset(), many=True).data,
            'quizzes': QuizSerializer(search_quizzes(q).to_queryset(), many=True).data,
        }
        return Response(data=data, status=status.HTTP_200_OK)
