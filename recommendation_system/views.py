from rest_framework.response import Response
from rest_framework.views import APIView

from recommendation_system.utils import get_recommended_quizzes


class RecommendQuizzesView(APIView):

    def get(self, request, *args, **kwargs):
        return Response(data=get_recommended_quizzes(request.user.id))
