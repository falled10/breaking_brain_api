from mixer.backend.django import mixer
from django.urls import reverse

from breaking_brain_api.tests import BaseAPITest
from quizzes.models import Quiz, Question, Option


class QuizTest(BaseAPITest):

    def setUp(self):
        self.quiz = mixer.blend(Quiz)
        self.question = mixer.blend(Question, quiz=self.quiz)
        self.option = mixer.blend(Option, question=self.question)

    def test_get_list_of_quizes(self):
        resp = self.client.get(reverse('quizzes-list'))
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.data['count'], 1)
        self.assertEqual(resp.data['results'][0]['id'], self.quiz.id)
        self.assertEqual(resp.data['results'][0]['title'], self.quiz.title)
        self.assertEqual(resp.data['results'][0]['questions'][0]['id'],
                         self.quiz.id)
        self.assertEqual(resp.data['results'][0]['questions'][0]['options'][0]['id'],
                         self.option.id)

    def test_get_single_quiz(self):
        resp = self.client.get(reverse('quizzes-detail', args=(self.quiz.id,)))
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.data['id'], self.quiz.id)
        self.assertEqual(resp.data['title'], self.quiz.title)
        self.assertEqual(resp.data['questions'][0]['id'],
                         self.quiz.id)
        self.assertEqual(resp.data['questions'][0]['options'][0]['id'],
                         self.option.id)

    def test_get_non_existed_quiz(self):
        resp = self.client.get(reverse('quizzes-detail', args=(123123,)))
        self.assertEqual(resp.status_code, 404)
