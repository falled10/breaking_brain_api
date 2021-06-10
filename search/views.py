from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from quizzes.serializers import LessonSerializer, QuizSerializer
from search.utils import search_lessons, search_quizzes
from search.schemas import SearchSchema


class SearchView(APIView):
    permission_classes = (AllowAny,)

    @swagger_auto_schema(
        operation_summary="Search by whole content",
        operation_description="Search by lessons and quizzes",
        responses={200: SearchSchema}
    )
    def get(self, request, *args, **kwargs):
        q = request.GET.get('q', '')
        data = {
            'lessons': LessonSerializer(search_lessons(q).to_queryset(), many=True).data,
            'quizzes': QuizSerializer(search_quizzes(q).to_queryset(), many=True).data,
        }
        return Response(data=data, status=status.HTTP_200_OK)
