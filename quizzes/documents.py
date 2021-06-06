from django_elasticsearch_dsl import Document, fields
from django_elasticsearch_dsl.registries import registry

from quizzes.models import Quiz, Tag, Lesson


@registry.register_document
class QuizDocument(Document):
    tags = fields.ObjectField(properties={
        'label': fields.TextField()
    })
    lessons = fields.ObjectField(properties={
        'title': fields.TextField()
    })

    class Index:
        name = 'quizzes'
        settings = {'number_of_shards': 1,
                    'number_of_replicas': 0}

    class Django:
        model = Quiz
        fields = ('title', 'description')
        related_models = (Tag, Lesson)

    def get_queryset(self):
        return super().get_queryset().prefetch_related('tags')

    def get_instances_from_related(self, related_instance):
        if isinstance(related_instance, Tag):
            related_instance: Tag
            return related_instance.quizzes.all()
        related_instance: Lesson
        return related_instance.quiz


@registry.register_document
class LessonDocument(Document):

    class Index:
        name = 'lessons'
        settings = {'number_of_shards': 1,
                    'number_of_replicas': 0}

    class Django:
        model = Lesson
        fields = ('title', 'body')
