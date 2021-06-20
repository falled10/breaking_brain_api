from django.db.models import Count, Q
from rest_framework import serializers

from quizzes.utils import has_bought_quiz
from recommendation_system.schemas import QuizSchema
from recommendation_system.utils import create_relation
from results.models import QuizResult, QuestionResult, OptionResult


class OptionResultSerializer(serializers.ModelSerializer):

    class Meta:
        model = OptionResult
        fields = ('option',)


class QuestionResultSerializer(serializers.ModelSerializer):
    options = OptionResultSerializer(many=True)

    class Meta:
        model = QuestionResult
        fields = ('quiz', 'question', 'options')

    def create(self, validated_data):
        if validated_data['quiz'].user != self.context['request'].user:
            raise serializers.ValidationError("You should choose your own quiz result.")
        options = validated_data.pop('options')
        question = super().create(validated_data)
        for option in options:
            OptionResult.objects.create(question=question, option=option['option'])
        return question


class QuizResultSerializer(serializers.ModelSerializer):

    class Meta:
        model = QuizResult
        fields = ('id', 'quiz', 'result', 'is_finished', 'created_at')
        read_only_fields = ('id', 'result', 'created_at')

    def validate_quiz(self, value):
        if not has_bought_quiz(value, self.context['request'].user):
            raise serializers.ValidationError("You should buy this quiz first")
        return value

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)

    def update(self, instance, validated_data):
        is_finished = not instance.is_finished and validated_data.get('is_finished')
        obj = super().update(instance, validated_data)
        if is_finished:
            questions = obj.questions.all()
            result = 0
            for question in questions:
                result += question.options.aggregate(
                    right_count=Count('id', filter=Q(option__is_right=True)))['right_count'] or 0
            obj.result = result
            obj.save(update_fields=('result',))
            create_relation(QuizSchema.from_orm(obj.quiz).dict(),
                            {'user_id': obj.user.id})
        return obj
