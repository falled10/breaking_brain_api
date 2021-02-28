from django.contrib import admin
from nested_inline.admin import NestedTabularInline, NestedModelAdmin

from quizzes.models import Quiz, Question, Option


class OptionInline(NestedTabularInline):
    model = Option
    extra = 1


class QuestionInline(NestedTabularInline):
    model = Question
    extra = 1
    inlines = (OptionInline,)


@admin.register(Quiz)
class QuizAdmin(NestedModelAdmin):
    inlines = (QuestionInline,)
