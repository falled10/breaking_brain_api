from elasticsearch_dsl import Q

from quizzes.documents import QuizDocument, LessonDocument


def search_lessons(phrase: str, page: int = 1, page_size: int = 30):
    from_result = (page - 1) * page_size
    to_result = from_result + page_size
    query = Q({
        "multi_match": {
            "query": phrase,
            "type": "most_fields",
            "fields": [
                "title",
            ]
        }
    }
    )
    return LessonDocument.search()[from_result:to_result].query(query)


def search_quizzes(phrase: str, page: int = 1, page_size: int = 30):
    from_result = (page - 1) * page_size
    to_result = from_result + page_size
    query = Q({
        "multi_match": {
            "query": phrase,
            "type": "most_fields",
            "fields": [
                "title",
                "tags.label",
                'lessons.title',
                'description'
            ]
        }
    }
    )
    return QuizDocument.search()[from_result:to_result].query(query)
