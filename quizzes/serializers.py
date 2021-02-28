from rest_framework import serializers

from quizzes.models import Question, Quiz, Option


class OptionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Option
        fields = ('id', 'label', 'is_right')


class QuestionSerializer(serializers.ModelSerializer):
    options = OptionSerializer(many=True, read_only=True)

    class Meta:
        model = Question
        fields = ('id', 'label', 'options')


class QuizSerializer(serializers.ModelSerializer):
    questions = QuestionSerializer(many=True, read_only=True)

    class Meta:
        model = Quiz
        fields = ('id', 'title', 'description', 'questions')
