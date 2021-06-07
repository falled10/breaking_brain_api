from elasticsearch_dsl import Q

from quizzes.documents import QuizDocument


def get_search_query(phrase: str, page: int = 1, page_size: int = 30):
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
