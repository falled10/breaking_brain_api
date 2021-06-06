from elasticsearch_dsl import Q

from quizzes.documents import QuizDocument


def get_search_query(phrase: str, page=1, page_size=30):
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
    return QuizDocument.search()[page-1 * page_size, page * page_size].query(query)
