from django.db import models

from authentication.models import User
from quizzes.models import Quiz, Question, Option


class QuizResult(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='results')
    result = models.PositiveIntegerField(default=0)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='results')
    is_finished = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'quiz_results'


class QuestionResult(models.Model):
    quiz = models.ForeignKey(QuizResult, on_delete=models.CASCADE, related_name='questions')
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='results')

    class Meta:
        db_table = 'questions_results'


class OptionResult(models.Model):
    question = models.ForeignKey(QuestionResult, on_delete=models.CASCADE, related_name='options')
    option = models.ForeignKey(Option, on_delete=models.CASCADE, related_name='results')

    class Meta:
        db_table = 'options_results'
