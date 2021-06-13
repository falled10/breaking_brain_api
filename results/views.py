from rest_framework import mixins
from rest_framework.decorators import action
from rest_framework.generics import CreateAPIView
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from breaking_brain_api.paginators import ResultSetPagination
from results.models import QuizResult, QuestionResult
from results.serializers import QuizResultSerializer, QuestionResultSerializer


class QuizResultViewSet(GenericViewSet, mixins.CreateModelMixin,
                        mixins.UpdateModelMixin, mixins.ListModelMixin,
                        mixins.RetrieveModelMixin):
    serializer_class = QuizResultSerializer
    pagination_class = ResultSetPagination

    def get_queryset(self):
        return QuizResult.objects.filter(user=self.request.user)

    @action(detail=True, methods=["GET"], url_name='last-question',
            url_path='last-question')
    def last_question(self, request, pk=None, *args, **kwargs):
        quiz_result = get_object_or_404(QuizResult, pk=pk)
        last_question = quiz_result.questions.order_by('-id').last()
        data = {
            'last_question_id': last_question.question.id if last_question else None
        }
        return Response(data=data)


class CreateQuestionResultView(CreateAPIView):
    serializer_class = QuestionResultSerializer
    queryset = QuestionResult.objects.all()
