from django.db import models


class Tag(models.Model):
    label = models.CharField(max_length=255)

    class Meta:
        db_table = 'tags'

    def __str__(self):
        return self.label


class Quiz(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    tags = models.ManyToManyField(Tag, related_name='quizzes')
    is_free = models.BooleanField(default=False)
    price = models.DecimalField(default=0, max_digits=5, decimal_places=2)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'quizzes'

    def __str__(self):
        return self.title


class Question(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='questions')
    label = models.CharField(max_length=255)

    class Meta:
        db_table = 'questions'


class Option(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='options')
    label = models.CharField(max_length=255)
    is_right = models.BooleanField(default=False)

    class Meta:
        db_table = 'options'
        unique_together = ['question', 'is_right']


class Lesson(models.Model):
    title = models.CharField(max_length=255)
    body = models.TextField()
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='lessons')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'lessons'
