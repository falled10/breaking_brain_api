from django.conf import settings
from py2neo import Relationship

from recommendation_system.models import User, Quiz
from recommendation_system.schemas import UserSchema, QuizSchema


def create_relation(quiz_data: dict, user_data: dict):
    quiz_data = QuizSchema(**quiz_data)
    user_data = UserSchema(**user_data)
    user = get_or_create_user(user_data)
    get_or_create_quiz(user, quiz_data)


def get_or_create_user(user_data: UserSchema):
    user = User.match(settings.GRAPH, user_data.user_id).first()
    if not user:
        user = User()
        user.user_id = user_data.user_id
        settings.GRAPH.push(user)
    return user


def get_or_create_quiz(user: User, quiz_data: QuizSchema):
    quiz = Quiz.match(settings.GRAPH, quiz_data.id).first()
    tx = settings.GRAPH.begin()
    if not quiz:
        quiz = Quiz()
        quiz.id = quiz_data.id
        quiz.title = quiz_data.title
        quiz.description = quiz_data.description
        quiz.is_free = quiz_data.is_free
        quiz.price = quiz_data.price
        quiz.created_at = quiz_data.created_at
        tx.create(quiz)
    query = "RETURN EXISTS("\
            "(:User {user_id: $user_id})-"\
            "[:PASSED]-(:Quiz {id: $quiz_id}))"
    relation_exists = settings.GRAPH.run(query, user_id=user.user_id, quiz_id=quiz_data.id).evaluate()
    if not relation_exists:
        tx.create(Relationship(user.__node__, 'PASSED', quiz.__node__))
        tx.create(Relationship(quiz.__node__, 'PASSED_BY', user.__node__))
    tx.commit()
    return quiz


def get_recommended_quizzes(user_id: int) -> list:
    query = "MATCH (u:User {user_id: $user_id})"\
            "-[:PASSED]->(:Quiz)<-[:PASSED]-(o:User) "\
            "MATCH (o:User)<-[:PASSED*1..5]->(rec:Quiz) "\
            "WHERE NOT EXISTS((u)-[:PASSED]->(rec)) RETURN DISTINCT rec"
    data = settings.GRAPH.run(query, user_id=user_id).data()
    return [quiz['rec'] for quiz in data]
