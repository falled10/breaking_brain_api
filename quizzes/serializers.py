from rest_framework import serializers


class LessonSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    title = serializers.CharField()
    body = serializers.CharField()
    updated_at = serializers.DateTimeField()


class TagSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    label = serializers.CharField()


class OptionSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    label = serializers.CharField()
    is_right = serializers.BooleanField()


class QuestionSerializer(serializers.Serializer):
    options = OptionSerializer(many=True, read_only=True)
    id = serializers.IntegerField()
    label = serializers.CharField()


class QuizSerializer(serializers.Serializer):
    tags = TagSerializer(many=True, read_only=True)
    lessons = LessonSerializer(many=True, read_only=True)
    id = serializers.IntegerField()
    title = serializers.CharField()
    description = serializers.CharField()


class BuyQuizSerializer(serializers.Serializer):
    confirmation = serializers.BooleanField()
    payment_method_id = serializers.CharField()
