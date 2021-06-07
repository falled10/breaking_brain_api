from mixer.backend.django import mixer
from django.urls import reverse
from django_elasticsearch_dsl.registries import registry

from breaking_brain_api.tests import BaseAPITest
from quizzes.models import Quiz, Lesson


class TestSearch(BaseAPITest):

    def setUp(self):
        self.quiz = mixer.blend(Quiz, title='something')
        self.other_quiz = mixer.blend(Quiz)
        self.lesson = mixer.blend(Lesson, quiz=self.other_quiz, title='something')
        registry.update(self.quiz)
        registry.update(self.lesson)
        registry.update_related(self.quiz)

    def tearDown(self):
        registry.delete(self.quiz)
        registry.delete(self.lesson)
        registry.delete_related(self.quiz)

    def test_search_by_all_indexes(self):
        url = f"{reverse('search')}?q=something"
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.data['lessons'][0]['id'], self.lesson.id)
        self.assertEqual(resp.data['lessons'][0]['title'], self.lesson.title)
        self.assertEqual(resp.data['quizzes'][0]['title'], self.quiz.title)

    def test_search_by_all_indexes_when_query_is_worong(self):
        url = f"{reverse('search')}?q=else"
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(len(resp.data['quizzes']), 0)
        self.assertEqual(len(resp.data['lessons']), 0)
