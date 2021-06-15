from authentication.models import User
from quizzes.models import Quiz


def has_bought_quiz(quiz: Quiz, user: User):
    """
    Check if user has bought quiz, or quiz is free
    """
    return quiz.is_free or user.bought_quizzes.filter(pk=quiz.pk).exists()
