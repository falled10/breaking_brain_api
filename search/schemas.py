from rest_framework import serializers

from quizzes.serializers import LessonSerializer, QuizSerializer


class SearchSchema(serializers.Serializer):
    lessons = LessonSerializer(many=True)
    quizzes = QuizSerializer(many=True)
