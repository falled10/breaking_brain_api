from django.contrib import admin
from nested_inline.admin import NestedTabularInline, NestedModelAdmin

from quizzes.models import Quiz, Question, Option, Tag, Lesson


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
    filter_horizontal = ('tags',)


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    pass


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    pass
